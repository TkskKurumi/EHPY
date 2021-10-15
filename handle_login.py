from os import path
import requests
try:
    from io_util import updatejson,dumpjson,loadjson
    from request_wrapper import sess,proxy
    from paths import *
except Exception:
    from .paths import *
    from .io_util import updatejson,dumpjson,loadjson   
    from .request_wrapper import sess,proxy

if(not(path.exists(cookie_pth))):
    print('You have not logged in')
    username=input("username:")
    password=input("password:")
    r=requests.post(r'https://forums.e-hentai.org/index.php?act=Login&CODE=01',data={'UserName':username,'PassWord':password,'CookieDate':1},proxies=proxy)
    header1={}
    header1['Accept']='text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    header1['Accept-Encoding']='gzip, deflate, br'
    header1['Accept-Language']='zh-CN,zh;q=0.9'
    header1['Connection']='keep-alive'
    header1['Sec-Fetch-User']="?1"
    header1['Sec-Fetch-Mode']="navigate"
    header1['Sec-Fetch-Site']="none"
    header1['Upgrade-Insecure-Requests']="1"
    dumpjson(cookie_pth,r.cookies.get_dict())
    print('\n'.join(["%s: %s"%(i,j) for i,j in header1.items()]))
    r=requests.get(r'https://exhentai.org/?f_cats=767',headers=header1,proxies=proxy,cookies=r.cookies)
    
    updatejson(cookie_pth,r.cookies.get_dict())
    cookie_json=loadjson(cookie_pth)
else:
    cookie_json=loadjson(cookie_pth)
    
for i,j in cookie_json.items():
    sess.cookies.set(i,j)