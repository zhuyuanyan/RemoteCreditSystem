# coding:utf-8
from lxml import etree#导入lxml库
from RemoteCreditSystem.tools.SimpleCache import SimpleCache

#权限种类
resource_dict = {
					'create':{'name':'创建','code':"1"},
					'change':{'name':'修改','code':"2"},
					'browse':{'name':'浏览','code':"4"}
				}

def getresource(type):
	return resource_dict[type]

def readXml(path):
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
		simplecache.set(id,{'id':id,'code':code,'name':name,'url':url,'levels':'1','pId':root.get("id"),'operations':0,'open':1})
		
		for level_2 in level_1:#遍历article元素的所有子元素(这里是指article的author，name，volume，year等)
			id=level_2.get("id")#用.get("属性名")可以得到article元素相应属性的值
			code=level_2.get("code")
			name=level_2.get("name")
			url=level_2.get("url")
			operations = level_2.get("operations")
			index = level_2.get("index")
			simplecache.set(id,{'id':id,'code':code,'name':name,'url':url,'levels':'2','pId':level_1.get("id"),'index':index,'operations':0,'open':0})
			
			for level_3 in level_2:#遍历article元素的所有子元素(这里是指article的author，name，volume，year等)
				id=level_3.get("id")#用.get("属性名")可以得到article元素相应属性的值
				code=level_3.get("code")
				name=level_3.get("name")
				url=level_3.get("url")
				operations = level_3.get("operations")
				simplecache.set(id,{'id':id,'code':code,'name':name,'url':url,'levels':'3','pId':level_2.get("id"),'operations':0,'open':1})
				for type in operations.split("|"):
					op_id = ''.join([id,'_',getresource(type)['code']])
					simplecache.set(op_id,{'id':op_id,'code':code,'name':getresource(type)['name'],'url':url,'levels':'4','pId':id,'operations':getresource(type)['code'],'open':1})
					           
	#for key_cache in simplecache:            
	#	print key_cache,":",data[key_cache]