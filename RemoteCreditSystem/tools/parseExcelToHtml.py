#coding:utf-8
from jpype import *
import os
_HERE = os.path.dirname(__file__)

def parser(path,index):
    #java.lang.System.out.println("hello world")
    TXL = JPackage('cn').JXLReadExcel  
    jd = TXL()
    return jd.readExcelToHtml(path,index,True).replace("\n", "<br>")
