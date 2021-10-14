try:
    from paths import work_pth
    from io_util import *
except Exception:
    from .paths import work_pth
    from .io_util import *
from os import path
debug_save_pth=path.join(work_pth,'debug_save')

def debug_save_html(name,content):
    name=name.replace(":",";").replace("/","_").replace("?","&").replace("\\","_")
    pth=path.join(debug_save_pth,name)
    savetext(pth,content)