import re, requests,urllib3,json,os, argparse
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
htmlToKeepRegex=r"id=\"__NEXT_DATA__\" type=\"application\/json\">(.*)"
slackHeaders={'Accept':'application/vnd.github.cloak-preview+json'}
from db import *
from proxy import *
from datetime import datetime
eventLog = []

def send_notif(toSend):
  params_raw = {"text": toSend }
  params = json.dumps(params_raw)
  r = requests.post("https://hooks.slack.com/services/XXXX/XXXXXX", data=params, headers=slackHeaders, verify=False)
   
def cleanDuplicates(mylist):
	return list(dict.fromkeys(mylist))
    
def doRequest(urlStr):
    response = requests.get(url=urlStr)
    if response.status_code == 200:
        return response.text
    else:
        return "error"

def monitorProjects():
    global conn  
    regex = r"\"id\":\"(\w+)\","
    htmlResponse=doRequest("https://immunefi.com/explore/")
    for match in re.finditer(regex, htmlResponse, re.MULTILINE):
        project=match.group(1)
        if not doesProjectExists(conn,project):
            send_notif("New Project : https://immunefi.com/bounty/" + project + "/")
            now=datetime.now().strftime("%Y-%m-%d %H:%M")
            content=(now,project,"")
            addURL(conn, content)
            monitor(project,False)


def monitor(project,monitor):
    global conn   
    global eventLog
    try:
        #Grab text containing all the assets
        urlAssets="https://immunefi.com/bounty/" + project + "/"
        htmlResponse=doRequest(urlAssets)
        #Only keep the JSON part
        matches = re.search(htmlToKeepRegex, htmlResponse, re.MULTILINE)
        htmlCode = matches.group(0)

        if htmlCode != "error":
            projectURLs=[]
            regexURLs = r'(http|https):\/\/[a-zA-Z0-9.\/?=_%:-]*'
            for match in re.finditer(regexURLs, htmlCode, re.MULTILINE):
                URL=match.group(0)
                projectURLs.append(URL)
        else:
            print("Impossible to get URL")
        projectURLs=cleanDuplicates(projectURLs)
        for URL in projectURLs:
            if not isExistingURL(conn,URL):
                now=datetime.now().strftime("%Y-%m-%d %H:%M")
                content=(now,project,URL)
                print(project + " " + URL)
                addURL(conn, content)
                if monitor :
                    eventLog.append("[" + now + "] - " + project + " - " + URL + "\n")
                    send_notif("New URL for " + project + " : " + URL)
                analyzeProxy(URL)
    except:
        #Project gone
        if project !="sushiswap" and project != "yearnfinance":
            send_notif("Project gone :\n https://immunefi.com/bounty/" + project)
            deleteProject(conn,project)

def listProjects():
    with open('clean_projects.txt') as f:
        projects = f.read().splitlines()
        for project in projects:
            print(project)
            monitor(project,False)

def logger(file,message):
    f=open(file,'a')
    f.write(message + "\n")
    f.close()

def addProxy():
    global conn
    global eventLog
    now=datetime.now().strftime("%Y-%m-%d %H:%M")
    for url in getAllURLs(conn):
        try:
            project=getProjectFromURL(conn,url)
            chain=getChain(url)
            if chain != "NA" :
                proxyAddress,implAddress=checkProxy(url)
                if implAddress != "0x":
                    content=(now,project,url,proxyAddress,implAddress,chain)
                    if not doesProxyContractExist(conn,proxyAddress):
                        eventLog.append("[" + now + "] - Addition - " + url +  " - " +  implAddress + "\n")
                        addProxyContract(conn,content)
                        addProxyContractHistory(conn,content)
        except Exception as e:
            print("Error : " + str(e))
            pass

def analyzeProxy(url):
    global conn
    global eventLog
    now=datetime.now().strftime("%Y-%m-%d %H:%M")
    project=getProjectFromURL(conn,url)
    chain=getChain(url)
    if chain != "NA" :
        proxyAddress,implAddress=checkProxy(url)
        if implAddress != "0x":
            content=(now,project,url,proxyAddress,implAddress,chain)
            if not doesProxyContractExist(conn,proxyAddress):
                eventLog.append("[" + now + "] - Addition - " + url +  " - " +  implAddress + "\n")
                addProxyContract(conn,content)
                addProxyContractHistory(conn,content)
                #send_notif("New Proxy for " + project + " : " + url)

def monitorProxy():
    global eventLog
    urls=getAllProxiesURLs(conn)
    now=datetime.now().strftime("%Y-%m-%d %H:%M")
    for url in urls:
        chain=getProxyChain(conn,url)
        project=getProxyProject(conn,url)
        proxyAddress=getProxyAddress(conn,url)
        previousImpl=getProxyImplementation(conn,url)
        ignore,currentImplAddress=checkProxy(url)
        if previousImpl != currentImplAddress and currentImplAddress !="0x":
            eventLog.append("[" + now + "] - Update - " + url + " - " + previousImpl + " - " +  currentImplAddress + "\n")
            print(proxyAddress + " - " + previousImpl + " - " +  currentImplAddress)
            content=(now,project,url,proxyAddress,currentImplAddress,chain)
            updateProxy(conn,proxyAddress,currentImplAddress,chain)
            content=(now,project,url,currentImplAddress,previousImpl,chain)
            addProxyContractHistory(conn,content)
            send_notif(project + " , New implementation on Proxy : " + url)


def main():
    global eventLog
    global conn
    parser = argparse.ArgumentParser()
    parser.add_argument('--add', help='Add Immunefi project', action='store_true')
    parser.add_argument('--monitor', help='Monitor existing Immunefi project', action='store_true')
    parser.add_argument('--monitorprojects', help='Check for new projects', action='store_true')
    parser.add_argument('--proxyMonitor', help='Monitor proxies to see if there are upgrades', action='store_true')
    parser.add_argument('--proxyAdd', help='Parse new URL from Immunefi and update proxy DB', action='store_true')
    parser.add_argument('--project', help='Chain to choose')
    parser.add_argument('--test', help='test', action='store_true')
    args = parser.parse_args()
    if (args.monitor):
        projects=getAllProjects(conn)
        for project in projects : 
            print("Checking project " + project)
            monitor(project,True)
    elif (args.add):
        if (args.project):
            monitor(args.project,False)
        else:
            print("/!\ Need project")
    elif (args.proxyMonitor):
        monitorProxy()
    elif (args.proxyAdd):
        addProxy()
    elif (args.test):
        monitorProjects()
    elif (args.monitorprojects):
        monitorProjects()
    else:
        print("/!\ Incorrect action (Add,Monitor)")
        send_notif(" , New implementation on Proxy : ")
    if eventLog :
        eventLog = cleanDuplicates(eventLog)
        eventToLog=''.join(eventLog)
        logger("/tmp/immunefi.log",eventToLog.rstrip())

if __name__ == "__main__":
  main()