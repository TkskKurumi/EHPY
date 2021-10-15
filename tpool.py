from concurrent.futures import ThreadPoolExecutor
thread_pool=ThreadPoolExecutor(max_workers=500)
tpool=thread_pool
doing=set()
def submit_thread(func,*args,**kwargs):
    
    name='%s(%s,%s)'%(func,','.join([str(i) for i in args]),','.join(["%s=%s"%(k,v) for k,v in kwargs.items()]))
    def inner(func=func,args=args,kwargs=kwargs):
        doing.add(name)
        ret=func(*args,**kwargs)
        if(name in doing):
            doing.remove(name)
        return ret
    return thread_pool.submit(inner)