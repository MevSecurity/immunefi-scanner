import requests, json,urllib3,re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headersEtherscan = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
}

regexURL= r"0x[0-9a-fA-F]{40}"
regexProxyImpl = r"ABI for the implementation contract at <a href='/address/(\w+)#code"

def doRequestEtherscan(urlStr):
    response = requests.get(url=urlStr, headers=headersEtherscan)
    if response.status_code == 200:
        return response.text
    else:
        return "error"

def getChain(URL):
    chain="NA"
    if "etherscan" in URL:
        chain="ETH"
    elif "bscscan" in URL:
        chain="BSC"
    elif "polygonscan" in URL:
        chain="MATIC"
    elif "ftmscan" in URL:
        chain="FTM"
    elif "optimistic" in URL:
        chain="OETH"
    elif "arbiscan" in URL:
        chain="AETH"
    elif "arbiscan" in URL:
        chain="AETH"
    elif "moonriver" in URL:
        chain="MOVR"
    elif "moonscan" in URL:
        chain="GLMR"
    elif "aurorascan" in URL:
        chain="A-ETH"
    elif "gnosisscan" in URL:
        chain="GNO"
    elif "snowtrace" in URL:
        chain="AVAX"
    return chain

def checkProxy(URL):
    #Get Proxy address from Etherscan URL
    matches = re.search(regexURL, URL, re.MULTILINE)
    #Get proxy info from Etherscan
    proxyURL = matches.group(0)
    try:
        htmlResponse=doRequestEtherscan(URL)
        matches = re.search(regexProxyImpl, htmlResponse, re.MULTILINE)
        proxyImpl = matches.group(1)
        return proxyURL,proxyImpl
    except:
        return proxyURL,"0x"

