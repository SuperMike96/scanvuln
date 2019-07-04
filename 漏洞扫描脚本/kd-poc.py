import threading
import requests
import re


with open('kd10.txt', 'r') as file:
    lines = file.readlines()
    file.close()


def kd(url, features, res_list, save):
    try:
        header = {
            "User-Agent": " Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"}
        jion_url = url.split('\n')[0] + features
        # print(jion_url)
        res = requests.get(jion_url, timeout=2)
        # lock.acquire()
        print('[Try] %s' % jion_url)
        # lock.release()
        # res.raise_for_status()
        if 'kindsoft' in res.text:
            lock.acquire()
            print('Success %s' % url)
            res_list.append(url)
            save.write('%s\t%s\n' % (url.split('\n')[0], features))
            lock.release()
        # res_list[url] = kd_res[0]
        # kd_res = re.findall(r'( KindEditor .*? )', res.text)
        # if len(kd_res) != 0:
        #     lock.acquire()
        #     res_list[url] = kd_res[0]
        #     print('[Success] %s' % url)
        #     lock.release()
        #     return kd_res[0]
        else:
            return False
    except:
        return False


res_list = []
lock = threading.Lock()


# 特征列表
features_list = ['/scripts/kindeditor/kindeditor.js', '/script/kindeditor/kindeditor.js',
                 '/ke4/kindeditor-all-min.js', '/kindeditor/kindeditor.js', '/kindeditor/kindeditor-min.js']
theads = []

save = open('kindeditor-res1.txt', 'w+')

for url in lines:
    for features in features_list:
        t = threading.Thread(target=kd, args=(url, features, res_list, save))
        theads.append(t)

for t in theads:
    t.start()
    t.join()

# for i in range(len(lines)):
#     print('[Try %s ] %s' % (i + 1, lines[i]))
#     tmp = kd(lines[i], res_list)

save.close()
print(res_list)
