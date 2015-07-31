#coding:utf-8
from jpype import *
import os
_HERE = os.path.dirname(__file__)

def parser(path,index):
    #java.lang.System.out.println("hello world")
    print "----------14"
    TXL = JPackage('cn').JXLReadExcel  
    print "----------15"
    jd = TXL()
    print "----------16"
    return jd.readExcelToHtml(path,index,True).replace("\n", "<br>")
