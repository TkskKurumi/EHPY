import requests_cache
import requests
import re
from glob import glob
import shutil
import traceback
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
    from misc import legalize_path
except ImportError:
    from .misc import legalize_path

try:
    from handle_login import cookie_json
    from tpool import *
    from request_wrapper import *
    from data import *
    import parsers
except Exception as e:
    import traceback
    traceback.print_exc()
    from .handle_login import cookie_json
    from .tpool import *
    from .request_wrapper import *
    from . import parsers
    from .data import *
if(__name__ == '__main__'):

    def submit_gallery(gid, token):
        savedata('downloading', '%s-%s' % (gid, token), 'id', [gid, token])
        savedata('downloading', '%s-%s' % (gid, token), 'is_downloading', True)
        savedata('downloading', '%s-%s' % (gid, token), 'url',
                 parsers.concat_gallery_url(gid, token))

        def inner(gid, token):
            try:
                g = parsers.gallery(gid, token)
            except Exception as e:
                import traceback
                traceback.print_exc()
                raise e

            tasks = g.download_tasks()
            print("submit %s" % g.title)
            for i in tasks:
                try:
                    result = i.result()
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    raise e
                print("Downloaded", i.result())
            savedata('downloading', '%s-%s' %
                     (gid, token), 'is_downloading', False)
        thread_pool.submit(inner, gid, token)
    try:
        downloading = getdata('downloading')
    except Exception:
        downloading = {}
    for _, i in downloading.items():
        gid, token = i['id']
        is_downloading = i['is_downloading']
        if(is_downloading):
            submit_gallery(gid, token)
    print("EHPY CLI")
    while(True):
        try:
            inp = input("> ")

            pattern_gallery = r'(\d{3,})/([0-9a-f]+)/'
            find_gallery = re.findall(pattern_gallery, inp)
            if(find_gallery):
                print('Downloading galleries')
                for gid, token in find_gallery:
                    submit_gallery(gid, token)
            elif(inp in ['exit', "quit"]):
                exit()
            elif(inp == 'show threads'):
                from tpool import doing
                print(doing)
            elif(inp == "gen_hexo"):
                gen_pth  = path.join(work_pth, "gen_hexo_posts")
                galleries = getdata("galleries")
                if(galleries):
                    print("Dump to", gen_pth)
                    if(path.exists(gen_pth)):
                        print("Clean", gen_pth)
                        shutil.rmtree(gen_pth)
                    os.makedirs(gen_pth)
                    for k, v in galleries.items():
                        downloaded_pth = v["download_path"]
                        title = v['title']
                        title_jpn = v.get("title_jpn", title)
                        print("Copy and generate for", title_jpn)
                        basename = legalize_path(title, True).replace(" ", "-")
                        basename = basename.replace("[", "-").replace("]","-")
                        dst = path.join(gen_pth, basename)
                        shutil.copytree(downloaded_pth, dst)
                        with open(path.join(gen_pth, basename+".md"), "w", encoding='utf-8') as f:
                            prt = lambda *args, **kwargs : print(*args, file=f, **kwargs)
                            prt("---")
                            prt("title:", title.replace("[", "(").replace("]", ")"))
                            prt("---")
                            prt("# ", title_jpn)
                            
                            lsdir = os.listdir(dst)
                            for idx, file in enumerate(lsdir):
                                prt("![](%s)"%file)
                                if(idx == 0):
                                    prt("<!--more-->")
                        
                    print("Done generating for hexo")
                else:
                    print("no galleries")
            else:
                print("Unknown operation.")
        except Exception:
            traceback.print_exc()
