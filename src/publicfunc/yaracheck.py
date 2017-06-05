#coding=utf-8

import sys, os
import yara
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, pyqtSignal
import sqlite3

reload(sys)
sys.setdefaultencoding( "utf-8" )

def is_file_packed(filename):
    i = 0 # 统计数量/Number of Statistics
    ret = [] # 保存结果/Save Results
    # 没有编译过yara规则时/When the Yara Rule is Not Compiled
    if not os.path.exists("rules_compiled/Packers"):
	os.mkdir("rules_compiled/Packers")
	for n in os.listdir("rules/Packers/"):
            rule = yara.compile("rules/Packers/" + n)
            rule.save("rules_compiled/Packers/" + n)
            rule = yara.load("rules_compiled/Packers/" + n)
            m = rule.match(filename)
            if m:
                ret += m
    # 已经生成了yara规则的二进制文件/Binary File for Yara Rule has Been Generated
    else:
        print "Using compiled file ..."
        for n in os.listdir("rules_compiled/Packers/"):
            rule = yara.load("rules_compiled/Packers/" + n)
            m = rule.match(filename)
            if m:
                ret += m
    return ret

def is_malicious_document(filename):
    #i = 0 # 统计数量/Number of Statistics
    ret = [] # 保存结果/Save Results
    if not os.path.exists("rules_compiled/Malicious_Documents"):
        os.mkdir("rules_compiled/Malicious_Documents")
	for n in os.listdir("rules/Malicious_Documents/"):
            rule = yara.compile("rules/Malicious_Documents/" + n)
            rule.save("rules_compiled/Malicious_Documents/" + n)
            rule = yara.load("rules_compiled/Malicious_Documents/" + n)
            m = rule.match(filename)
            if m:
                return m
    else:
        print "Using compiled file ..."
        for n in os.listdir("rules_compiled/Malicious_Documents/"):
            rule = yara.load("rules_compiled/Malicious_Documents/" + n)
            m = rule.match(filename)
            if m:
                ret += m
    return ret

def is_antidb_antivm(filename):
    #i = 0 # 统计数量/Number of Statistics
    ret = [] # 保存结果/Save Results
    if not os.path.exists("rules_compiled/Antidebug_AntiVM"):
        os.mkdir("rules_compiled/Antidebug_AntiVM")
        for n in os.listdir("rules/Antidebug_AntiVM/"):
            rule = yara.compile("rules/Antidebug_AntiVM/" + n)
            rule.save("rules_compiled/Antidebug_AntiVM/" + n)
            rule = yara.load("rules_compiled/Antidebug_AntiVM/" + n)
            m = rule.match(filename)
            if m:
                ret += m
    else:
        print "Using compiled file ..."
        for n in os.listdir("rules_compiled/Antidebug_AntiVM/"):
            rule = yara.load("rules_compiled/Antidebug_AntiVM/" + n)
            m = rule.match(filename)
            if m:
                ret += m
    return ret

def check_crypto(filename):
    #i = 0 # 统计数量/Number of Statistics
    ret = [] # 保存结果/Save Results
    if not os.path.exists("rules_compiled/Crypto"):
        os.mkdir("rules_compiled/Crypto")
        for n in os.listdir("rules/Crypto/"):
            rule = yara.compile("rules/Crypto/" + n)
            rule.save("rules_compiled/Crypto/"  + n)
            rule = yara.load("rules_compiled/Crypto/" + n)
            m = rule.match(filename)
            if m:
                ret += m
    else:
        print "Using compiled file ..."
        for n in os.listdir("rules_compiled/Crypto/"):
            rule = yara.load("rules_compiled/Crypto/" + n)
            m = rule.match(filename)
            if m:
                ret += m
    return ret

def is_webshell(filename):
    #i = 0 # 统计数量/Number of Statistics
    ret = [] # 保存结果/Save Results
    if not os.path.exists("rules_compiled/Webshells"):
        os.mkdir("rules_compiled/Webshells")
        for n in os.listdir("rules/Webshells/"):
            rule = yara.compile("rules/Webshells/" + n)
            rule.save("rules_compiled/Webshells/" + n)
            rule = yara.load("rules_compiled/Webshells/" + n)
            m = rule.match(filename)
            if m:
                ret += m
    else:
        print "Using compiled file ..."
        for n in os.listdir("rules_compiled/Webshells/"):
            rule = yara.load("rules_compiled/Webshells/" + n)
            m = rule.match(filename)
            if m:
                ret += m
    return ret

def is_malware(filename):
    #i = 0 # 统计数量/Number of Statistics
    ret = [] # 保存结果/Save Results
    if not os.path.exists("rules_compiled/malware"):
        os.mkdir("rules_compiled/malware")
        for n in os.listdir("rules/malware/"):
            if not os.path.isdir("rules/malware/" + n):
                rule = yara.compile("rules/malware/" + n)
                rule.save("rules_compiled/malware/" + n)
                rule = yara.load("rules_compiled/malware/" + n)
                m = rule.match(filename)
                if m:
                    ret += m
            #Sony Special
            #elif os.path.isdir("rules/malware/" + n):
            #    if not os.path.exists("rules_compiled/malware/Operation_Blockbuster"):
            #        os.mkdir("rules_compiled/malware/Operation_Blockbuster")
            #        for n in os.listdir("rules/malware/Operation_Blockbuster/"):
            #            if n is not 'mastersig':
            #                rule = yara.compile("rules/malware/Operation_Blockbuster/" + n)
            #                rule.save("rules_compiled/malware/Operation_Blockbuster/" + n)
            #                rule = yara.load("rules_compiled/malware/Operation_Blockbuster/" + n)
            #                m = rule.match(filename)
            #                if m:
            #                    ret += m
            #            #elif n=='mastersig':
            #            #    pass
            #except:
            #    print "Internal Yara Error"
    else:
        print "Using compiled file ..."
        for n in os.listdir("rules_compiled/malware/"):
            rule = yara.load("rules_compiled/malware/" + n)
            m = rule.match(filename)
            if m:
                ret += m
    return ret

def is_custom_rules(filename):
    #i = 0 # 统计数量/Number of Statistics
    ret = [] # 保存结果/Save Results
    if not os.path.exists("custom/customrules/"):
        os.mkdir("custom/customrules/")
        for n in os.listdir("custom/customrules/"):
            rule = yara.compile("custom/customrules/" + n)
            rule.save("custom/customrules/" + n)
            rule = yara.load("custom/customrules/" + n)
            m = rule.match(filename)
            if m:
                ret += m
    else:
        print "Using compiled file ..."
        for n in os.listdir("rules_compiled/customrules/"):
            rule = yara.load("rules_compiled/customrules/" + n)
            m = rule.match(filename)
            if m:
                ret += m
            #except yara.Error, e:
            #    print "Internal Yara Error", e.args[0]
    return ret

class CheckPacker(QtCore.QThread):
    numberSignal = QtCore.pyqtSignal(int, str)
    valueSignal  = QtCore.pyqtSignal(int)

    def __init__(self, filename, index, md5, parent=None):
        super(CheckPacker, self).__init__(parent)
        self.filename = filename
        self.index    = index
        self.md5      = str(md5)

    def write2YaraDB(self, md5, result):
        try:
            sqlconn = sqlite3.connect("../db/detected.db")
        except sqlite3.Error, e:
            print "sqlite connect failed", "\n", e.args[0]
            return -1
        sqlcursor = sqlconn.cursor()
        try:
            print "insert to yara packed"
            sqlcursor.execute("update yara_result set packed=? where md5=?", (str(result), self.md5))
            sqlconn.commit()
            sqlconn.close()
            return 1
        except sqlite3.Error, e:
            print "sqlite exec err", "\n", e.args[0]
            return -1

    def run(self):
        print self.index
        pkdresult = is_file_packed(self.filename)
        result1 = []
        result  = {}
        if pkdresult:
            print "get pkdresult!"
            for n in pkdresult:
                # 能输出描述则输出描述/Can Output Description, Output Description
                # 否则直接输出规则名/Otherwise the Direct Output Rule Name
                # try:
                #     result1.append("{} - {}".format(n, n.meta['description']))
                # except:
                result1.append(str(n))
                # 最终直接输出评估结果，数据库里存详细内容/Final Direct Output Evaluation Results, Database Store Details
            result["packed"] = result1
            ret = self.write2YaraDB(self.md5, result)
            if ret:
                self.valueSignal.emit(1)
        else:
            print "no match"

class CheckMalware(QtCore.QThread):
    numberSignal = QtCore.pyqtSignal(int, str)
    valueSignal  = QtCore.pyqtSignal(int)

    def __init__(self, filename, md5, parent=None):
        super(CheckMalware, self).__init__(parent)
        self.filename = filename
        self.md5      = str(md5)

    def write2YaraDB(self, md5, result):
        try:
            sqlconn = sqlite3.connect("../db/detected.db")
        except sqlite3.Error, e:
            print "sqlite connect failed", "\n", e.args[0]
            return -1
        sqlcursor = sqlconn.cursor()
        try:
            print "insert to yara malware"
            sqlcursor.execute("insert into yara_result (md5, _default) values(?, ?)", (self.md5, str(result)))
            sqlconn.commit()
            sqlconn.close()
            return 1
        except sqlite3.Error, e:
            print "sqlite exec err", "\n", e.args[0]
            return -1

    def run(self):
        # 匹配到spyeye的基本是debug文件/The Basic Debug File is Matched to SpyEye
        malresult = is_malware(self.filename)
        atiresult = is_antidb_antivm(self.filename)
        result1 = []
        result2 = []
        result  = {}
        if None == (malresult or atiresult):
            print "malw and atidbg no match"
            self.write2YaraDB(self.md5, "null")
            self.valueSignal.emit(-1)
            return
        if malresult:
            for n in malresult:
                # try:
                #     result1.append("{} - {}".format(n, n.meta['description']))
                # except:
                result1.append(str(n))
            result["malware"] = result1
        if atiresult:
            for n in atiresult:
                # try:
                #     result2.append("{} - {}".format(n, n.meta['description']))
                # except:
                result2.append(str(n))
            result["antidbg"] = result2
        ret = self.write2YaraDB(self.md5, result)
        if ret:
            self.valueSignal.emit(1)

class CheckCrypto(QtCore.QThread):
    numberSignal = QtCore.pyqtSignal(int, str)
    valueSignal  = QtCore.pyqtSignal(int)

    def __init__(self, filename, md5, parent=None):
        super(CheckCrypto, self).__init__(parent)
        self.filename = filename
        self.md5      = str(md5)

    def write2YaraDB(self, md5, result):
        try:
            sqlconn = sqlite3.connect("../db/detected.db")
        except sqlite3.Error, e:
            print "sqlite connect failed", "\n", e.args[0]
            return -1
        sqlcursor = sqlconn.cursor()
        try:
            print "insert to yara crypto"
            sqlcursor.execute("update yara_result set crypto=? where md5=?", (str(result), self.md5))
            sqlconn.commit()
            sqlconn.close()
            return 1
        except sqlite3.Error, e:
            print "sqlite exec err", "\n", e.args[0]
            return -1

    def run(self):
        cptresult = check_crypto(self.filename)
        result1 = []
        result  = {}
        if cptresult:
            print "Encryption Used!"
            for n in cptresult:
                # try:
                #     result1.append("{} - {}".format(n, n.meta['description']))
                # except:
                result1.append(str(n))
            result["crypto"] = result1
            ret = self.write2YaraDB(self.md5, result)
        else:
            print "no match"

class CheckWebshell(QtCore.QThread):
    numberSignal = QtCore.pyqtSignal(int, str)
    valueSignal  = QtCore.pyqtSignal(int)

    def __init__(self, filename, md5, parent=None):
        super(CheckWebshell, self).__init__(parent)
        self.filename = filename
        self.md5      = str(md5)

    def write2YaraDB(self, md5, result):
        try:
            sqlconn = sqlite3.connect("../db/detected.db")
        except sqlite3.Error, e:
            print "sqlite connect failed", "\n", e.args[0]
            return -1
        sqlcursor = sqlconn.cursor()
        try:
            print "insert to yara malware"
            sqlcursor.execute("insert into yara_result (md5, _default) values(?, ?)", (self.md5, str(result)))
            sqlconn.commit()
            sqlconn.close()
            return 1
        except sqlite3.Error, e:
            print "sqlite exec err", "\n", e.args[0]
            return -1

    def run(self):
        shellresult = is_webshell(self.filename)
        result1 = []
        result  = {}
        if shellresult:
            print "Found webshell artifact!"
            for n in shellresult:
                # try:
                #     result1.append("{} - {}".format(n, n.meta['description']))
                # except:
                result1.append(str(n))
            result["webshell"] = result1
            ret = self.write2YaraDB(self.md5, result)
            if ret:
                self.valueSignal.emit(1)
        else:
            print "no match"
            self.write2YaraDB(self.md5, "null")

class Checkcustom(QtCore.QThread):
    numberSignal = QtCore.pyqtSignal(int, str)
    valueSignal  = QtCore.pyqtSignal(int)

    def __init__(self, filename, md5, parent=None):
        super(Checkcustom, self).__init__(parent)
        self.filename = filename
        self.md5      = str(md5)

    def write2YaraDB(self, md5, result):
        try:
            sqlconn = sqlite3.connect("../db/detected.db")
        except sqlite3.Error, e:
            print "sqlite connect failed", "\n", e.args[0]
            return -1
        sqlcursor = sqlconn.cursor()
        try:
            print "insert to yara crypto"
            sqlcursor.execute("update yara_result set crypto=? where md5=?", (str(result), self.md5))
            sqlconn.commit()
            sqlconn.close()
            return 1
        except sqlite3.Error, e:
            print "sqlite exec err", "\n", e.args[0]
            return -1

    def run(self):
        cptresult = is_custom_rules(self.filename)
        result1 = []
        result  = {}
        if cptresult:
            print "get custom!"
            for n in cptresult:
                # try:
                #     result1.append("{} - {}".format(n, n.meta['description']))
                # except:
                result1.append(str(n))
            result["custom"] = result1
            # ret = self.write2YaraDB(self.md5, result)
        else:
            print "custom no match"
        print result
