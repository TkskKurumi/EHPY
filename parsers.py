import re
try:
    from request_wrapper import *
except Exception as e:
    from .request_wrapper import *
def as_html(url_or_html):
    if(url_or_html.startswith("http")):
        html=gettext(url_or_html)
    else:
        html=gettext(url_or_html)
    return html
try:
    from parsers_gallery import gallery,concat_gallery_url
except Exception:
    from .parsers_gallery import gallery,concat_gallery_url

def parse_listing(url_or_html):
    html=as_html(url_or_html)
    f_all=re.findall(r'<div class="glthumb" id="it[\s\S]+?<div onclick=".+?"',html)
    #myio.savetext(os.path.join(workpath,'temp.list'),'\n\n'.join(nmsl))
    ret=[]
    for i in f_all:
        title=re.findall(r'alt="([\s\S]+?)"',i)[0]
        gid=re.findall(r'gid=(\d+?)&amp',i)[0]
        token=re.findall(r'&amp;t=(.+?)&amp',i)[0]
        preview_pic=re.findall(r'src="(https://exhentai.org/.+?jpg)"',i)[0]
        #preview_pic=re.sub(r'(jpg|png)_\d+.jpg','jpg_l.jpg',preview_pic)
        ret.append({'title':title,'gid':gid,'token':token,'preview_pic':preview_pic})
            
    return ret
    