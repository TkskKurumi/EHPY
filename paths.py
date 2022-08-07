from os import path
work_pth = path.join(path.dirname(__file__), 'files')
cache_pth = path.join(work_pth, 'sqlcache')
cookie_pth = path.join(work_pth, 'cookies.json')
data_pth = path.join(work_pth, 'datas.json')
__all__ = ['work_pth', 'cache_pth', 'cookie_pth', 'data_pth']
