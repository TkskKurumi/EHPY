from os import path
import json
import os
def dumpjson(filename,j):
    with open(filename,'w') as f:
        json.dump(j,f)
    return j
def updatejson(filename,j,empty_if_dne=True):
    if(not path.exists(filename)):
        if(empty_if_dne):
            original_json={}
        else:
            raise FileNotFoundError(filename)
    else:
        with open(filename,'r') as f:
            original_json=json.load(f)
    original_json.update(j)
    with open(filename,'w') as f:
        json.dump(original_json,f)
    return original_json
def loadjson(filename):
    with open(filename,'r') as f:
        ret=json.load(f)
    return ret
def savetext(filename,content):
    if(not path.exists(path.dirname(filename))):
        os.makedirs(path.dirname(filename))
    with open(filename,'w',encoding='utf-8') as f:
        f.write(content)
    f.close()
def savebin(filename,content):
    if(not path.exists(path.dirname(filename))):
        os.makedirs(path.dirname(filename))
    with open(filename,"wb") as f:
        f.write(content)
    return