import requests
import re
import json
import os
import urllib
import argparse
import traceback

parser = argparse.ArgumentParser(description='fuck dxonline')
parser.add_argument('-start',type=int)
parser.add_argument('-end',type=int)
args = parser.parse_args()

# 全局信息 
# 下面这三个变量是为了让程序能登进这个系统的 不会干别的事情 所以放心填:)
wyQiantai_name = urllib.parse.quote("这里要填你的姓名")
wyQiantai_num = "这里要填你的学号"
PHPSESSID = "这里要填你的PHPSESSID"

def myrequest(url):
    querystring = {}
    method = "GET"
    headers = {
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        'cache-control': "no-cache",
        'postman-token': "524d22a5-6f66-096b-08df-ccef375e8ebc",
        }
    cookies={
        'PHPSESSID':PHPSESSID,\
        'wyQiantai_name':wyQiantai_name,
        'wyQiantai_num':wyQiantai_num
    }
    response = requests.request(method, url, headers=headers, params=querystring, cookies=cookies)
    rtxt = response.text
    return rtxt   

def fuck_one_dk(url):
    # 首先，我们抓取这个视频的页面
    content = myrequest(url)
    
    # 我们从这个页面里抽几个id，用来构造看完视频的请求。
    conid = re.findall(r"var conid=\"(.+?)\";",content)[0]
    sing = re.findall(r"var sing=\"(.+?)\";",content)[0]
    vid = re.findall(r"vid:(.+?),tid:",content)[0]
    tid = re.findall(r"tid:(.+?)},function",content)[0]
    hours = re.findall(r"var hours=\"(.+?)\";",content)[0]
    
    # 然后, 我们给它做一下页面初始化.
    av_sh = f'curl --location --request POST \'http://dxonline.ruc.edu.cn/index.php?s=/Index/add_videonum.html\' \
    --header \'Accept: */*\think \' \
    --header \'X-Requested-With: XMLHttpRequest\' \
    --header \'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36\' \
    --header \'Content-Type: application/x-www-form-urlencoded; charset=UTF-8\' \
    --header \'Cookie: PHPSESSID={PHPSESSID}; wyQiantai_name={wyQiantai_name}; wyQiantai_num={wyQiantai_num}\' \
    --data-urlencode \'tid={tid}\' \
    --data-urlencode \'vid={vid}\''
    os.system(av_sh)
    
    # 再然后，我们开始播放视频
    d = myrequest(f"http://dxonline.ruc.edu.cn/index.php?s=/Videoclock/index.html&videokey={vid}&videonum=1&ct=0")
    d = json.loads(d)
    print(d)
    ct = d['data']['create_time']
    
    # 接下来，我们点中间弹出的三次按钮
    print(myrequest(f"http://dxonline.ruc.edu.cn/index.php?s=/Videoclock/index.html&videokey={vid}&videonum=2&ct={ct}"))
    print(myrequest(f"http://dxonline.ruc.edu.cn/index.php?s=/Videoclock/index.html&videokey={vid}&videonum=3&ct={ct}"))
    print(myrequest(f"http://dxonline.ruc.edu.cn/index.php?s=/Videoclock/index.html&videokey={vid}&videonum=4&ct={ct}"))
    
    # 最后，我们看完了
    p_sh = f"curl --location --request POST 'http://dxonline.ruc.edu.cn/index.php?s=/Index/gethours.html' \
        --header 'Accept: */*' --header 'X-Requested-With: XMLHttpRequest' --header 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36' --header 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
                --header 'Cookie: PHPSESSID={PHPSESSID}; wyQiantai_name={wyQiantai_name}; wyQiantai_num={wyQiantai_num}' \
                    --data-urlencode \'conid={conid}==' --data-urlencode 'ct={ct}' --data-urlencode 'hours={hours}' \
                        --data-urlencode 'name={wyQiantai_name}' --data-urlencode 'num={wyQiantai_num}' --data-urlencode 'sing={sing}'"
    os.system(p_sh)
    # fuck success!

def main():
    startid = args.start
    endid = args.end
    for _id in range(startid, endid + 1):
        try:
            pageurl = f"http://dxonline.ruc.edu.cn/index.php?m=Index&a=vedio_cont&id={_id}"
            fuck_one_dk(pageurl)
            print(f"the {pageurl} success!")
        except:
            print(f"error while fucking {pageurl}")
            traceback.print_exc()

if __name__ == "__main__":
    main()
