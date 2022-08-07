import re
import traceback

try:
    from misc import dict_format
    from request_wrapper import *
    from debug_util import *
    from tpool import thread_pool, submit_thread
    from paths import work_pth
    from io_util import *
except Exception:
    from .request_wrapper import *
    from .debug_util import *
    from .tpool import thread_pool, submit_thread
    from .paths import work_pth
    from .io_util import *
    from .misc import dict_format


def as_html(url_or_html):
    if(url_or_html.startswith("http")):
        html = gettext(url_or_html)
    else:
        html = gettext(url_or_html)
    return html


def concat_gallery_url(gid, token, page=None):
    if(not page):
        return r'https://exhentai.org/g/%s/%s/' % (gid, token)
    else:
        return r'https://exhentai.org/g/%s/%s/?p=%d' % (gid, token, page)


def get_title(html):
    gn_pattern = r'<h1 id="gn">([\s\S]+?)</h1>'
    gj_pattern = '<h1 id="gj">([\s\S]+?)</h1>'
    f_all_gn = re.findall(gn_pattern, html)
    f_all_gj = re.findall(gj_pattern, html)
    # print(f_all)
    ret = {}
    if(f_all_gn):
        ret['title'] = f_all_gn[0]
    if(f_all_gj):
        ret['title_jpn'] = f_all_gj[0]
    return ret


class mydict(dict):
    def __getattr__(self, name):
        if(name in self):
            return self[name]
        else:
            raise AttributeError(name)

    def __repr__(self):
        return '\n'.join(dict_format(self))

    def __str__(self):
        return self.__repr__()

    def __setattr__(self, name, value):
        self[name] = value


class single_page(mydict):
    def __init__(self, url):
        try:
            super().__init__()
            html = gettext(url)

            try:
                iurl = re.findall(
                    r'<img id="img" src="(.+?)" style="', html)[0].replace('&amp;', '&')
            except IndexError as e:
                raise Exception(
                    "error parsing single_page (%s) (%s)" % (url, e))
            try:
                iurl_f = re.findall(
                    r'<a href="(https://exhentai.org/fullimg.php\?gid=\d+?&amp;page=\d+?&amp;key=.+?)">Download', html)[0]

            except IndexError as e:
                iurl_f = iurl
                print(url, 'have no full image')
            self['image_url_original'] = iurl_f
            self['image_url'] = iurl
            self.url = self.referer = url
        except Exception:
            traceback.print_exc()

    def refresh(self):
        sess.delete_url(url, proxies=proxy, method='GET')
        self.__init__(self.url)


class gallery_page(mydict):
    def __init__(self, url):
        super().__init__()
        html = submit_thread(gettext, url).result()
        try:
            pattern = r'https://exhentai.org/s/.{10}/\d+-\d+'
            self['single_pages'] = []
            single_page_urls = re.findall(pattern, html)
            single_page_tasks = []
            for url in single_page_urls:
                task = submit_thread(single_page, url)
                single_page_tasks.append(task)
            for i in single_page_tasks:
                self.single_pages.append(i.result())
        except Exception as e:
            traceback.print_exc()


class gallery(mydict):
    def from_url(url):
        pattern = r'(\d{3,})/([0-9a-f]+)/'
        fall = re.findall(pattern, url)
        if(fall):
            gid, token = fall[0]
            return gallery(gid, token)
        else:
            raise ValueError('Unknown gallery url')

    def __init__(self, gid, token):
        try:

            super().__init__()
            self['gid'] = gid
            self['token'] = token

            url0 = concat_gallery_url(gid, token)
            html0 = gettext(url0)

            self.update(get_title(html0))
            print('%s parsing' % self.title)
            self['preview_pic'] = re.findall(
                r'background:transparent url\((.+?)\)', html0)[0]

            temp_pagenum = re.findall(
                r'Showing (\d{1,4}) - (\d{1,4}) of (\d{1,4})', html0)

            st, ed, tot = [int(i) for i in temp_pagenum[0]]

            step = ed-st+1

            gallery_page_tasks = []
            print('%s submit gallery_page' % self.title)
            for st in range(1, tot+1, step):
                page = (st-1)//step

                task = submit_thread(
                    gallery_page, concat_gallery_url(gid, token, page))
                gallery_page_tasks.append(task)
            gallery_pages = [i.result() for i in gallery_page_tasks]

            self.pages_flat = {"map_referer": {},
                               "image_urls": [], "image_urls_original": []}
            self.pages = []
            print('%s gather pages' % self.title)
            for _gallery_page in gallery_pages:

                for _single_page in _gallery_page.single_pages:
                    iurl = _single_page.image_url
                    iurl_f = _single_page.image_url_original
                    url = _single_page.url
                    self.pages_flat["map_referer"][iurl] = url
                    self.pages_flat["map_referer"][iurl_f] = url
                    self.pages_flat["image_urls"].append(iurl)
                    self.pages_flat["image_urls_original"].append(iurl_f)
                    self.pages.append(_single_page)
        except Exception as e:
            traceback.print_exc()

    def download_single_page(self, idx, pth, retries=3):
        print('downloading %s-%04d' % (self.title, idx))
        page = self.pages[idx]
        iurl = page.image_url
        referer = page.url
        r = None
        while((r is None) or (not r.ok) and retries > 0):
            retries -= 1
            r = sess.get(iurl, headers={
                         "Referer": referer, 'referer': referer}, proxies=proxy)
            if(not r.ok):
                page.refresh()
        if(not r.ok):
            return 'fail'
        cont_type = r.headers.get("Content-Type", "png")

        ext = '.png'
        for i in cont_type.split(";"):
            if(i.endswith("png")):
                ext = '.png'
            elif(i.endswith('jpeg')):
                ext = '.jpg'

        dst = path.join(pth, "%s-%04d" % (self.gid, idx+1)+ext)
        savebin(dst, r.content)
        return dst

    def download_tasks(self, pth=None):
        if(pth is None):
            title = self.title
            title = title.replace('"', "'").replace("<", "[").replace(">", "]")
            for i in r'/\:*?|':
                title = title.replace(i, "_")
            pth = path.join(work_pth, 'downloads', '%s-%s' % (self.gid, title))
        tasks = []
        for idx, _ in enumerate(self.pages):
            tasks.append(submit_thread(self.download_single_page, idx, pth))
        return tasks
