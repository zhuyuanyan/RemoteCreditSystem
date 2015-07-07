# coding:utf-8
from lxml import etree#导入lxml库
from RemoteCreditSystem.tools.SimpleCache import SimpleCache
from RemoteCreditSystem.tools.StaticDictCache import StaticDictCache
from RemoteCreditSystem.tools.DynDictCache import DynDictCache
from RemoteCreditSystem import db
#权限种类
resource_dict = {
					'create':{'name':'创建','code':"1"},
					'change':{'name':'修改','code':"2"},
					'browse':{'name':'浏览','code':"4"}
				}

def getresource(type):
	return resource_dict[type]

#读取菜单
def readMenuXml(path):
	#简单缓存
	# Initialize
	SimpleCache()
	# Getting instance
	simplecache = SimpleCache.getInstance()

	tree = etree.parse(path)#将xml解析为树结构
	root = tree.getroot()#获得该树的树根
	
	for level_1 in root:#这样便可以遍历根元素的所有子元素(这里是article元素)
		id=level_1.get("id")#用.get("属性名")可以得到article元素相应属性的值
		code=level_1.get("code")
		name=level_1.get("name")
		url=level_1.get("url")
		operations = level_1.get("operations")
		if(id == None):
			continue
		simplecache.set(id,{'id':id,'code':code,'name':name,'url':url,'levels':'1','pId':root.get("id"),'operations':0,'open':1})
		
		for level_2 in level_1:#遍历article元素的所有子元素(这里是指article的author，name，volume，year等)
			id=level_2.get("id")#用.get("属性名")可以得到article元素相应属性的值
			code=level_2.get("code")
			name=level_2.get("name")
			url=level_2.get("url")
			operations = level_2.get("operations")
			index = level_2.get("index")
			if(id == None):
				continue
			simplecache.set(id,{'id':id,'code':code,'name':name,'url':url,'levels':'2','pId':level_1.get("id"),'index':index,'operations':0,'open':0})
			
			for level_3 in level_2:#遍历article元素的所有子元素(这里是指article的author，name，volume，year等)
				id=level_3.get("id")#用.get("属性名")可以得到article元素相应属性的值
				code=level_3.get("code")
				name=level_3.get("name")
				url=level_3.get("url")
				operations = level_3.get("operations")
				if(id == None):
					continue
				simplecache.set(id,{'id':id,'code':code,'name':name,'url':url,'levels':'3','pId':level_2.get("id"),'operations':0,'open':1})
				for type in operations.split("|"):
					op_id = ''.join([id,'_',getresource(type)['code']])
					simplecache.set(op_id,{'id':op_id,'code':code,'name':getresource(type)['name'],'url':url,'levels':'4','pId':id,'operations':getresource(type)['code'],'open':1})
					           
	#for key_cache in simplecache:            
	#	print key_cache,":",simplecache[key_cache]
	
#读取静态数据字典
def readStaticDictXml(path):
	# Initialize
	StaticDictCache()
	# Getting instance
	staticdictcache = StaticDictCache.getInstance()
	
	tree = etree.parse(path)#将xml解析为树结构
	root = tree.getroot()#获得该树的树根
	
	for level_1 in root:#这样便可以遍历根元素的所有子元素(这里是article元素)
		name=level_1.get("name")#用.get("属性名")可以得到article元素相应属性的值
		title=level_1.get("title")
		if(name == None):
			continue
		staticdictcache.set(name,{'name':name,'title':title})
		
		children = []
		for level_2 in level_1:#遍历article元素的所有子元素(这里是指article的author，name，volume，year等)
			name=level_2.get("name")#用.get("属性名")可以得到article元素相应属性的值
			title=level_2.get("title")
			if(name == None):
				continue
			children.append({'name':name,'title':title})
		tmp = staticdictcache.get(level_1.get("name"))
		tmp['children'] = children
		staticdictcache.set(level_1.get("name"),tmp)
		
	#for key_cache in staticdictcache:            
	#	print key_cache,":",staticdictcache[key_cache]
	
#读取动态数据字典
def readDynDictXml(path):
	# Initialize
	DynDictCache()
	# Getting instance
	dyndictcache = DynDictCache.getInstance()
	
	tree = etree.parse(path)#将xml解析为树结构
	root = tree.getroot()#获得该树的树根
	
	for level_1 in root:#这样便可以遍历根元素的所有子元素(这里是article元素)
		name=level_1.get("name")#用.get("属性名")可以得到article元素相应属性的值
		title=level_1.get("title")
		if(name == None):
			continue
		dyndictcache.set(name,{'name':name,'title':title})
		
		ls = db.session.execute(level_1.text.strip()).fetchall()
		
		children = []
		for obj in ls:
			children.append({'name':obj.name,'title':obj.title})
		tmp = dyndictcache.get(name)
		tmp['children'] = children
		dyndictcache.set(name,tmp)
		
	#for key_cache in dyndictcache:            
	#	print key_cache,":",dyndictcache[key_cache]
			