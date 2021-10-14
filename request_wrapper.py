import requests_cache
import cloudscraper
from datetime import timedelta
from PIL import Image
try:
    from paths import work_pth, cache_pth
except Exception:
    from .paths import work_pth, cache_pth
proxy={'http':'http://127.0.0.1:1081','https':'http://127.0.0.1:1081'}
cache_backend=requests_cache.backends.sqlite.SQLiteCache(cache_pth,expire_after=timedelta(hours=1),cache_control=True)




sess=requests_cache.CachedSession('CachedSession', backend = cache_backend)
sess.proxies.update(proxy)
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.18 Safari/537.36','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8;,application/signed-exchange','Accept-Encoding':'gzip, deflate, br','Host':'exhentai.org','Accept-Language':'zh-CN,zh;q=0.9',"Sec-Fetch-Site":"same-origin", "Sec-Fetch-Mode":"no-cors",'Connection':'keep-alive'}
sess.headers.update(headers)
def gettext(*args,**kwargs):
    r=sess.get(proxies=proxy,*args,**kwargs)
    return r.text
def getbin(*args,**kwargs):
    r=sess.get(proxies=proxy,*args,**kwargs)
    return r.content
def getimage(*args,**kwargs):
    content=getbin(proxies=proxy,*args,**kwargs)
    from io import BytesIO
    f=BytesIO()
    f.write(content)
    f.seek(0)
    return Image.open(f)