import requests
import json
import time
import random
import hashlib

url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
headers = {
    'Referer': 'http://fanyi.youdao.com/',
    'Cookie': 'OUTFOX_SEARCH_USER_ID=985180348@10.169.0.84; JSESSIONID=aaag_TPaA69Dm9vym1Gzx; OUTFOX_SEARCH_USER_ID_NCOO=290841985.32830364; ___rl__test__cookies=1607942391307',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

i = input("请输入要翻译的文字：")
lts = str(int(time.time()*1000))
salt = lts + str(random.randint(0, 9))
sign = hashlib.md5(("fanyideskweb" + i + salt + "Tbh5E8=q6U3EXe+&L[4c@").encode()).hexdigest()
data = {
    'i': i,
    'from': 'AUTO',
    'to': 'AUTO',
    'smartresult': 'dict',
    'client': 'fanyideskweb',
    'salt': salt,  # changed
    'sign': sign,  # changed
    'lts': lts,  # changed
    'bv': '6a11b3e0f30132e487c3cc180ff627a2',
    'doctype': 'json',
    'version': '2.1',
    'keyfrom': 'fanyi.web',
    'action': 'FY_BY_REALTlME'
}
res = requests.post(url, headers=headers, data=data)
dic = json.loads(res.content.decode())

if "translateResult" in dic:
    print(dic["translateResult"][0][0]["tgt"])
else:
    print('翻译出错。。。')
