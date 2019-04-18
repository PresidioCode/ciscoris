[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/levensailor/py-cisco-ris)

# ciscoris

Uses Realtime Information Service (RIS) to capture registration status of Cisco IP Phones on CUCM
https://developer.cisco.com/docs/sxml/#risport70-api-reference

#### Install with pip or clone repo

```bash
pip install ciscoris
```

#### import ris, logcollection or other classes
```py
from ciscoris import ris
```

#### specify your CUCM details
```py
cucm = os.getenv('cucm', '10.10.10.10')
version = os.getenv('version', '11.5')
risuser = os.getenv('risuser', 'risadmin')
rispass = os.getenv('rispass', 'p@ssw0rd')
```

#### instanciate your RIS object
```py
ris = ris(username=risuser,password=rispass,cucm=cucm,cucm_version=version)
```

#### input an array of phones

```py
phones = ['SEPF8A5C59E0F1C', 'SEP1CDEA78380DE', 'SEP01CD4EF58980']
```

#### input an array of "process nodes" or nodes which run Callmanager service
```py
subs = ['sub1', 'sub2', 'sub3']
```

#### you can use the related `ciscoaxl` library grab process nodes via API.
```py
def getSubs():
    nodes = axl.listProcessNodes()
    if nodes['success']:
        return nodes['response']

subs = getSubs()
```

#### group phones into 1000 and check registrations per group
```py
limit = lambda phones, n=1000: [phones[i:i+n] for i in range(0, len(phones), n)]

groups = limit(phones)
for group in groups:
    registered = ris.checkRegistration(group, subs)
    user = registered['LoginUserId']
    regtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(registered['TimeStamp']))
    for item in registered['IPAddress']:
        ip = item[1][0]['IP']

    for item in registered['LinesStatus']:
        primeline = item[1][0]['DirectoryNumber']
    name = registered['Name']

    print('name: '+name)
    print('user: '+user)
    print('primary dn: '+primeline)
    print('ip address: '+ip)
    print('registration time: '+regtime)
```
