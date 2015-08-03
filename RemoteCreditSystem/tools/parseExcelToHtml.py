#coding:utf-8
from jpype import *
import os
_HERE = os.path.dirname(__file__)


def parser(path,index):

    # if not isJVMStarted():
    # 	startJVM('/usr/java/jdk1.6.0_45/jre/lib/i386/client/libjvm.so',"-ea",'-Djava.class.path=/data/www/rcs/RemoteCreditSystem/ext_class/ReadExcel.jar')
    TXL = JPackage('cn').JXLReadExcel  
    jd = TXL()
    result = jd.readExcelToHtml(path,index,True).replace("\n", "<br>")
    return result


