import requests_cache
import requests,re,traceback
from os import path
try:
    from io_util import updatejson, dumpjson, loadjson
except Exception:
    from .io_util import updatejson, dumpjson, loadjson
try:
    from paths import work_pth, cache_pth
except Exception:
    from .paths import work_pth, cache_pth



try:
    from handle_login import cookie_json
    from tpool import *
    from request_wrapper import *
except Exception as e:
    from .handle_login import cookie_json
    from .tpool import *
    from .request_wrapper import *
    
import parsers
if(__name__=='__main__'):



    def submit_gallery(gid,token):
        print(gid,token)
        g=parsers.gallery(gid,token)
        tasks=g.download_tasks()
        print("submit %s"%g.title)
        for i in tasks:
            print("Downloaded",i.result())
        
    print("EHPY CLI")
    while(True):
        try:
            inp=input()
            
            pattern_gallery=r'(\d{3,})/([0-9a-f]+)/'
            find_gallery=re.findall(pattern_gallery,inp)
            if(find_gallery):
                print('Downloading galleries')
                for gid,token in find_gallery:
                    thread_pool.submit(submit_gallery,gid,token)
            if(inp=='exit'):
            
                exit()
                
        except Exception:
            traceback.print_exc()