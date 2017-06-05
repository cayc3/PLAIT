#coding=utf-8

import sys, os
import socket
import hashlib
import virus_total_apis
from PyQt5 import QtCore
sys.path.append("..")
from publicfunc.fileanalyze import FileAnalize, getFileInfo

class UploadFile(QtCore.QThread):
    finishSignal = QtCore.pyqtSignal(int, tuple)

    '''
    #@文件名
    @Filename
    #@用户公钥
    @User Public Key
    '''
    def __init__(self, filename, apikey, parent=None):
        super(UploadFile, self).__init__(parent)
        self.filename = str(filename)#.encode('cp936')
        self.apikey   = apikey
        print self.filename

    '''
    #检查网络，后期转移至common功能
    Check the Network, Later Transfer to Common Function
    '''
    def checkInternet(self):
        try:
            host = socket.gethostbyname("www.virustotal.com")
            s = socket.create_connection((host, 80), 2)
            print "internet ok"
            return True
        except:
            print "internet err"
        return False

    '''
    #virustotal api函数
    virustotal API Functions
    #解析json文件内容
    Parsing json File Contents
    #@apikey:用户公钥
    @apikey: User's Public Key
    #返回响应代码及检测结果
    Return Response Code and Test Results
    '''
    def virustotalApi(self, apikey):
        key = apikey
        result  = []
        result1 = [] # 检测到的引擎/Detected Engines
        result2 = [] # 未检测到的引擎/Engine Not Detected
        vt = virus_total_apis.PublicApi(key)
        md5 = hashlib.md5(open(self.filename, 'rb').read()).hexdigest()
        response = vt.get_file_report(md5)
        # print response # 所有结果/All Results
        print response["response_code"] # 网络响应码/Network Response Code
        if 204 == response["response_code"]: # 超出上传频率/Upload Frequency Exceeded
            print "204"
            return ("http_code", "", response["response_code"], "")
        response_code_ = response["results"]["response_code"]
        # print response_code_ # 返回信息响应代码/Return Information Response Code
        if 1 == response_code_:
            # 解析json回传内容/Parse JSON Return Content
            # 先显示报毒的引擎/Show the Engine of the Poison First
            for n in response["results"]["scans"]:
                if response["results"]["scans"][n]["detected"]:
                    result1.append("{} ^ {}".format(n, response["results"]["scans"][n]["result"]))
                else:
                    result2.append("{} ^ {}".format(n, response["results"]["scans"][n]["result"]))
            result = sorted(result1, key=str.lower) + sorted(result2, key=str.lower)
        elif -2 == response_code_:
            pass
        else:
            response = vt.scan_file(self.filename) # 32M limit
            if response["results"]["verbose_msg"]:
                result.append(response["results"]["verbose_msg"])
            else:
                result.append(response["results"]["permalink"])
        if 1 == response_code_:
            return ("scan_result", result, response["response_code"], response_code_)
        else:
            return ("permalink", result, response["response_code"], response_code_)
        # return ("scan_result", result, "http", response["response_code"], "code", response_code_)
        #  if response_code_ is 1 else ("permalink", result, "http", response["response_code"], "code", response_code_)
        # print ("scan_result", result) if response_code_ is 1 else ("permalink", result)

    def run(self):
        print "run"
        useless, baseinfo = getFileInfo(self.filename)
        infos = ("baseinfo", baseinfo)
        self.finishSignal.emit(2, infos)
        ret = self.checkInternet()
        if not ret:
            #self.finishSignal.emit(3, tuple(['网络连接失败...']))
            self.finishSignal.emit(3, tuple(['Network Connection Failed ...']))
            return
        msg = self.virustotalApi(self.apikey)
        self.finishSignal.emit(1, msg)

class AddFileToQqueu(QtCore.QThread):

    def __init__(self, filename, parent=None):
        super(AddFileToQqueu, self).__init__(parent)
        self.filename = filename

    def run(self):
        pass
