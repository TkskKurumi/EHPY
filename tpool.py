from concurrent.futures import ThreadPoolExecutor
import inspect
from threading import Lock


def new_pool():
    return ThreadPoolExecutor(max_workers=10)


pool_pool = {}
pool_pool_lock = Lock()


class locked:
    def __init__(self, lock):
        self.lock = lock

    def __enter__(self):
        self.lock.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.lock.release()
        return


def get_pool(key=None):
    with locked(pool_pool_lock):
        if(key is None):
            key = len(inspect.stack(0))
        if(key in pool_pool):
            return pool_pool[key]
        pool_pool[key] = new_pool()
        return pool_pool[key]


thread_pool = ThreadPoolExecutor(max_workers=500)
tpool = thread_pool
doing = set()


def submit_thread(func, *args, pool_key=None, **kwargs):

    name = '%s(%s,%s)' % (func, ','.join([str(i) for i in args]), ','.join(
        ["%s=%s" % (k, v) for k, v in kwargs.items()]))

    def inner(func=func, args=args, kwargs=kwargs):
        doing.add(name)
        ret = func(*args, **kwargs)
        if(name in doing):
            doing.remove(name)
        return ret
    return get_pool(pool_key).submit(inner)
