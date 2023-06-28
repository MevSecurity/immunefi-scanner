# immunefi-scanner
Scanner for new Immunefi projects, URLs, and proxies upgrades

# Start

1. Create Database
```text
GRANT ALL PRIVILEGES ON monitorImmunefi.* TO "user"@"localhost";
CREATE TABLE immunefiUrls ( 
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    date TEXT NOT NULL,
    project TEXT NOT NULL,
    URL TEXT,
    type TEXT,
);

CREATE TABLE proxyContracts ( 
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    date TEXT NOT NULL,
    project TEXT NOT NULL,
    url TEXT NOT NULL,
    proxyAddress TEXT NOT NULL,
    implAddress TEXT NOT NULL,
    chain TEXT NOT NULL
);


CREATE TABLE proxyContractsHistory ( 
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    date TEXT NOT NULL,
    project TEXT NOT NULL,
    url TEXT NOT NULL,
    proxyAddress TEXT NOT NULL,
    implAddress TEXT NOT NULL,
    chain TEXT NOT NULL
);
```

2. Update DB credentials in db.py
```text
conn = pymysql.connect(
  host="127.0.0.1",
  user="user",
  password="verystrongpassword",
  database='monitorImmunefi',
  cursorclass=pymysql.cursors.DictCursor
)
```

3. Change Slack hook in main.py
```python
def send_notif(toSend):
  params_raw = {"text": toSend }
  params = json.dumps(params_raw)
  r = requests.post("https://hooks.slack.com/services/XXXX/XXXXXX", data=params, headers=slackHeaders, verify=False)
```

4. Setup crontab
```bash
0 * * * * cd /opt/immunefi && python3 main.py --monitorprojects
0 */2 * * * cd /opt/immunefi && python3 main.py --proxyMonitor
40 * * * * cd /opt/immunefi && python3 main.py --monitor
```
