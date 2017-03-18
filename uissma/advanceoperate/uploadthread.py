#coding=utf-8

import socket
import hashlib
import virus_total_apis
from PyQt4 import QtCore, QtGui, Qt

class UploadFile(QtCore.QThread):
    finfishSignal = QtCore.pyqtSignal(int, tuple)

    '''
    @文件名
    @用户公钥
    '''
    def __init__(self, filename, apikey, parent=None):
        super(UploadFile, self).__init__(parent)
        self.filename = str(filename).encode('cp936')
        self.apikey   = apikey
        print self.filename

    '''
    检查网络，后期转移至common功能
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
    virustotal api函数
    解析json文件内容
    @apikey:用户公钥
    返回响应代码及检测结果
    '''
    def virustotalApi(self, apikey):
        key = apikey
        result = []
        vt = virus_total_apis.PublicApi(key)
        md5 = hashlib.md5(open(self.filename, 'rb').read()).hexdigest()
        response = vt.get_file_report(md5)
        # print response # 所有结果
        print response["response_code"]
        if 204 == response["response_code"]:
            print "204"
            pass
        response_code_ = response["results"]["response_code"]
        # print response_code_ # 二层响应代码
        if 1 == response_code_:
            # 解析json回传内容
            # 先显示报毒的引擎
            for n in response["results"]["scans"]:
                if response["results"]["scans"][n]["detected"]:
                    result.append("{} ^ {}".format(n, response["results"]["scans"][n]["result"]))
            for n in response["results"]["scans"]:
                if not response["results"]["scans"][n]["detected"]:
                    result.append("{} ^ {}".format(n, response["results"]["scans"][n]["result"]))
        elif -2 == response_code_:
            pass
        else:
            response = vt.scan_file(self.filename) # 32M limit
            result.append(response["results"]["permalink"])
        return ("scan_result", result) if response_code_ is 1 else ("permalink", result)
        # print ("scan_result", result) if response_code_ is 1 else ("permalink", result)

    def run(self):
        print "run"
        self.checkInternet()
        msg = self.virustotalApi(self.apikey)
        self.finfishSignal.emit(1, msg)

class AddFileToQqueu(QtCore.QThread):

    def __init__(self, filename, parent=None):
        super(AddFileToQqueu, self).__init__(parent)
        self.filename = filename

    def run(self):
        pass