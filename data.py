from paths import *
from io_util import *
from os import path
from threading import Lock
if(path.exists(data_pth)):
    datas = loadjson(data_pth)
else:
    datas = {}

lck = Lock()


def setdict(d, *args):
    if(len(args) == 2):
        key, value = args
        d[key] = value
    elif(len(args) > 2):
        key = args[0]
        dd = d.get(key, {})
        setdict(dd, *args[1:])
        d[key] = dd
    else:
        raise Exception("No enough args")


def getdict(d, *args):
    if(len(args) == 1):
        key = args[0]
        return d[key]
    else:
        key = args[0]
        dd = d[key]
        return getdict(dd, *args[1:])


def savedata(*args):
    lck.acquire()
    try:
        setdict(datas, *args)
        dumpjson(data_pth, datas)
    except Exception as e:
        lck.release()
        raise e
    lck.release()


def getdata(*args):
    return getdict(datas, *args)


if(__name__ == '__main__'):
    a = {}
    setdict(a, 'a', 'b', 'c')
    print(a, getdict(a, 'a', 'b'))
