# coding:utf-8
import collections
import HTMLParser
import cgi
from werkzeug.wrappers import Request, Response

"""
Simple local cache.
It saves local data in singleton dictionary with convenient interface

Examples of use:
    # Initialize
    SimpleCache({'data':{'example':'example data'}})
    # Getting instance
    c = SimpleCache.getInstance()

    c.set('re.reg_exp_compiled',re.compile(r'\W*'))
    reg_exp = c.get('re.reg_exp_compiled',default=re.compile(r'\W*'))

or

    c = SimpleCache.getInstance()
    reg_exp = c.getset('re.reg_exp_compiled',re.compile(r'\W*'))

or
    @scache
    def func1():
        return 'OK'

"""

class StaticDictCache(collections.OrderedDict):

    def __new__(cls,*args):
        if not hasattr(cls,'_instance'):
            cls._instance = dict.__new__(cls)
        else:
            raise Exception('StaticDictCache already initialized')
        return cls._instance

    @classmethod
    def getInstance(cls):
        if not hasattr(cls,'_instance'):
            cls._instance = dict.__new__(cls)
        return cls._instance

    def get(self,name,default=None):
        """Multilevel get function.
        Code:        
        Config().get('opt.opt_level2.key','default_value')
        """
        if not name: 
            return default
        levels = name.split('.')
        data = self            
        for level in levels:
            try:            
                data = data[level]
            except:
                return default

        return data

    def set(self,name,value):
        """Multilevel set function
        Code:        
        Config().set('opt.opt_level2.key','default_value')
        """
        levels = name.split('.')
        arr = self        
        for name in levels[:-1]:
            if not arr.has_key(name):         
                arr[name] = {}   
            arr = arr[name]
        arr[levels[-1]] = value

    def getset(self,name,value):
        """Get cache, if not exists set it and return set value
        Code:        
        Config().getset('opt.opt_level2.key','default_value')
        """
        g = self.get(name)
        if not g:
            g = value
            self.set(name,g)
        return g
    
    def getDict(self,dictName,selectValue,selectText):
        resStr = ""
        g = self.get(dictName)
        if g != None:
            tmp = g['children']
            for obj in tmp:
                if(selectValue != None and selectValue != ""):
                    if(selectValue == obj['name']):
                        resStr = "".join([resStr,"<option value='"+obj['name']+"' selected>"+obj['title']+"</option>"])
                    else:
                        resStr = "".join([resStr,"<option value='"+obj['name']+"'>"+obj['title']+"</option>"])
                elif(selectText != None and selectText != ""):
                    if(selectText == obj['title']):
                        resStr = "".join([resStr,"<option value='"+obj['name']+"' selected>"+obj['title']+"</option>"])
                    else:
                        resStr = "".join([resStr,"<option value='"+obj['name']+"'>"+obj['title']+"</option>"])
                else:
                    resStr = "".join([resStr,"<option value='"+obj['name']+"'>"+obj['title']+"</option>"])
        return resStr 
        
def scache(func):
    def wrapper(*args, **kwargs):
        cache = StaticDictCache.getInstance()
        fn = "scache." + func.__module__ + func.__class__.__name__ + \
             func.__name__ + str(args) + str(kwargs)        
        val = cache.get(fn)
        if not val:
            res = func(*args, **kwargs)
            cache.set(fn,res)
            return res
        return val
    return wrapper

