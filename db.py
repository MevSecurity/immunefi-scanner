import pymysql.cursors, time

conn = pymysql.connect(
  host="127.0.0.1",
  user="user",
  password="password",
  database='monitorImmunefi',
  cursorclass=pymysql.cursors.DictCursor
)

def addURL(conn, content):
    cur = conn.cursor()
    sql = ''' INSERT INTO immunefiUrls(date,project,URL) VALUES(%s,%s,%s) '''
    cur.execute(sql, content)
    conn.commit()
    return cur.lastrowid 

#Contracts - Exists?   
def isExistingURL(conn,URL):
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM `immunefiUrls` WHERE URL = '%s'" % URL)
    rows = cur.fetchone()['count(*)']
    #if rows, existing Contract
    if rows > 0:
        return True
    else:
        return False

def getAllProjects(conn):
    cur = conn.cursor()
    cur.execute("SELECT distinct project FROM `immunefiUrls`")
    projects = [item['project'] for item in cur.fetchall()]
    return projects  


def doesProjectExists(conn,project):
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM immunefiUrls WHERE project = '%s'" % (project))
    rows = cur.fetchone()['count(*)']
    #if rows, existing Address
    if rows > 0:
        return True
    else:
        return False    

def getAllURLs(conn):
    cur = conn.cursor()
    cur.execute("SELECT distinct url FROM immunefiUrls")
    urls = [item['url'] for item in cur.fetchall()]
    return urls  

def deleteProject(conn,project):
    cur = conn.cursor()
    cur.execute("DELETE FROM immunefiUrls WHERE project = '%s'" % project)
    conn.commit()
    
def getProjectFromURL(conn,URL):
    cur = conn.cursor()
    cur.execute("SELECT project FROM immunefiUrls WHERE url = '%s'" % URL)
    result = cur.fetchone()['project']
    return result

def getAllProxiesURLs(conn):
    cur = conn.cursor()
    cur.execute("SELECT distinct url FROM proxyContracts")
    urls = [item['url'] for item in cur.fetchall()]
    return urls  

def addProxyContract(conn, content):
    cur = conn.cursor()
    sql = ''' INSERT INTO proxyContracts(date,project,url,proxyAddress,implAddress,chain) VALUES(%s,%s,%s,%s,%s,%s) '''
    cur.execute(sql, content)
    conn.commit()
    return cur.lastrowid 

def addProxyContractHistory(conn, content):
    cur = conn.cursor()
    sql = ''' INSERT INTO proxyContractsHistory(date,project,proxyUrl,currentImpl,previousImpl,chain) VALUES(%s,%s,%s,%s,%s,%s) '''
    cur.execute(sql, content)
    conn.commit()
    return cur.lastrowid 

def updateProxy(conn,proxyAddress,implAddress,chain):
    cur = conn.cursor()
    cur.execute("UPDATE proxyContracts SET implAddress = '%s' where proxyAddress ='%s' and chain = '%s'" %  (implAddress,proxyAddress,chain))
    conn.commit()
    return 1

def doesProxyContractExist(conn,address):
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM proxyContracts WHERE proxyAddress = '%s'" % (address))
    rows = cur.fetchone()['count(*)']
    #if rows, existing Address
    if rows > 0:
        return True
    else:
        return False    

def getProxyImplementation(conn,url):
    cur = conn.cursor()
    cur.execute("SELECT implAddress FROM proxyContracts WHERE url = '%s'" %  (url))
    result = cur.fetchone()['implAddress']
    return result

def getProxyChain(conn,url):
    cur = conn.cursor()
    cur.execute("SELECT chain FROM proxyContracts WHERE url = '%s'" %  (url))
    result = cur.fetchone()['chain']
    return result

def getProxyProject(conn,url):
    cur = conn.cursor()
    cur.execute("SELECT project FROM proxyContracts WHERE url = '%s'" %  (url))
    result = cur.fetchone()['project']
    return result

def getProxyAddress(conn,url):
    cur = conn.cursor()
    cur.execute("SELECT proxyAddress FROM proxyContracts WHERE url = '%s'" %  (url))
    result = cur.fetchone()['proxyAddress']
    return result

def getProxyProject(conn,url):
    cur = conn.cursor()
    cur.execute("SELECT project FROM proxyContracts WHERE url = '%s'" %  (url))
    result = cur.fetchone()['project']
    return result