def mystr(i, quote='"'):
    if(isinstance(i, str)):
        return quote+i+quote
    else:
        return str(i)

def legalize_path(pth, replace_dir_split = False):
    pth = pth.replace('"', "'").replace("<", "[").replace(">", "]")
    if(replace_dir_split):
        for i in "\\/":
            pth = pth.replace(i, "_")
    for i in r':*?|':
        pth = pth.replace(i, "_")
    # pth = pth.join(work_pth, 'downloads', '%s-%s' % (self.gid, title))
    return pth
def dict_format(d, tabc="    "):
    ret = list()
    if(isinstance(d, dict)):
        ret.append("{")
        for i, j in d.items():
            j = dict_format(j)
            if(isinstance(i, str)):
                i = '"'+i+'"'
            if(len(j) == 1):
                j = j[0]

                ret.append(tabc+'%s: %s' % (i, j))
            else:
                ret.append(tabc+'%s:' % i)
                for k in j:
                    ret.append(tabc+k)
        ret.append("}")
    elif(isinstance(d, str)):
        return ['"'+d+'"']
    else:
        return [str(d)]
    return ret


if(__name__ == '__main__'):
    ls1 = ['1', '2', '114']
    dict1 = {'ls1': ls1, 'other_element': 'fuck'}
    ls2 = ['1', '2', dict1]
    dict2 = {'ls1': ls1, 'dict1': dict1}
    print("\n".join(dict_format(dict2)))
