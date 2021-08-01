import requests
import re
import base64
import sys

def rot47(s):
    x = []
    for i in range(len(s)):
        j = ord(s[i])
        if j >= 33 and j <= 126:
            x.append(chr(33 + ((j + 14) % 94)))
        else:
            x.append(s[i])
    return ''.join(x)

def decode_base64(data, altchars=b'+/'):
    data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += b'='* (4 - missing_padding)
    return base64.b64decode(data, altchars)

if not "ouo" in sys.argv[1]:
    print("Provide a ouo.io/press link as a first argument.")
    raise SystemExit

url = 'https://api.yuumari.com/ex-alb/'
destUrl = sys.argv[1:]
headers = { 
    'X-Requested-With': 'XMLHttpRequest',
    'X-Meow': "\x6d\x65\xba\x6f\x77",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Accept': '*/*',
    'Origin': 'chrome-extension://doiagnjlaingkmdjlbfalakpnphfmnoh',
    'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'
}

r = requests.get(url+"_/", headers=headers)
key = r.json().get('access_key')

hex2bin = bytes.fromhex(key)
base64decode = decode_base64(hex2bin)
apiKey = rot47(base64decode.decode('ascii'))

body = {'l': destUrl, 'u': apiKey}
r = requests.post(url, data=body, headers=headers)
print(r.json().get('result'))
