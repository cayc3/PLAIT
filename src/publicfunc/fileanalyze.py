#coding=utf-8

import sys, os
import time
from PyQt5 import QtCore, QtGui, QtWidgets
import hashlib
import numbers
import array
import math
from filebytes.pe import *
from filebytes.elf import *
from filebytes.mach_o import *
from filebytes.oat import *
import magic
import sqlite3
import re
import urlparse
import Queue
import threading
sys.path.append("../")
from globalset import ImpAlert

'''
#通用除法操作
Universal Division Operation
#可统一py2/3
Can Unify py2/3
'''
def commonDiv(a, b):
    if isinstance(a, numbers.Integral) and isinstance(b, numbers.Integral):
        return a // b
    else:
        return a / b

'''
#计算数据信息熵
Computational Data Entropy
#return熵值
Return Entropy Value
'''
def dataEntropy(data):
    if 0 == len(data):
        return 0.0
    arr = array.array('L', [0] * 256)
    for i in data:
        arr[i if isinstance(i, int) else ord(i)] += 1
    entropy = 0
    for i in arr:
        if i:
            p_i = commonDiv(float(i), len(data))
            entropy -= p_i * math.log(p_i, 2)
    return entropy

'''
#获取文件详细信息
Obtaining File Details
#infoo:原始数据 返回MD5 SHA1 SHA256 Size Type
Raw Data returns MD5 SHA1 SHA256 Size Type
#infof:格式化   返回Name Path ...
infof:Formatting   Return Name Path ...
'''
def getFileInfo(filename):
    infoo = [] # origin data
    infof = [] # format data
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            cfile = f.read()
            # 分割文件名与路径/Split File Name and Path
            p, f  = os.path.split(str(filename))#.decode('cp936'))
            # name   =
            infof.append("Name:\t{}".format(f))
            # path   =
            infof.append("Path:\t{}".format(p))
            # md5    =
            infoo.append(hashlib.md5(cfile).hexdigest())
            infof.append("MD5:\t{}".format(hashlib.md5(cfile).hexdigest()))
            # sha1   =
            infoo.append(hashlib.sha1(cfile).hexdigest())
            infof.append("SHA1:\t{}".format(hashlib.sha1(cfile).hexdigest()))
            # sha256 =
            infoo.append(hashlib.sha256(cfile).hexdigest())
            infof.append("SHA256:\t{}".format(hashlib.sha256(cfile).hexdigest()))
            # fsize  =
            infoo.append(os.path.getsize(filename))
            infof.append("Size:\t{} Bytes".format(os.path.getsize(filename)))
            # file_magic = magic.Magic(magic_file="../libs/magic.mgc")
            #ftype  =
            infoo.append(magic.from_file(filename, mime=False))
            infof.append("Type:\t{}".format(magic.from_file(filename, mime=False)))
        return infoo, infof
    else:
        print "file " + filename + "not exist!"
        return ["error"], ["error"]

class GetFileString:
    def __init__(self, filename):
        self.filename = filename
        self.chars    = b"A-Za-z0-9!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "
        self.short_t  = 4
        self.regexp   = '[{}]{{{},}}'.format(self.chars.decode(), self.short_t).encode()
        self.pattern  = re.compile(self.regexp)

        with open(self.filename, 'rb') as f:
            fbytes = self.fileProcess(f)
            fstr   = []
            for n in fbytes:
                fstr.append(n.decode())

        self.result = (self.checkIPAddr(fstr), self.checkWebsit(fstr), self.checkEmail(fstr))

    def fileProcess(self, filename):
        data = filename.read()
        return self.pattern.findall(data)

    def getResult(self):
        return self.result

    def checkIPAddr(self, strlist):
        ippattern = re.compile(r'((([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])[ (\[]?(\.|dot)[ )\]]?){3}([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5]))')
        f = filter(ippattern.match, strlist)
        return list(f)

    def checkWebsit(self, strlist):
        websit = []
        for n in strlist:
            try:
                netloc = urlparse.urlparse(n.split()[0]).netloc
                if netloc and "." in netloc and not netloc.startswith(".") and not netloc.endswith("."):
                    websit.append(netloc)
            except:
                pass
        websit = list(set(websit))
        return websit

    def checkEmail(self, strlist):
        email = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
        f = filter(email.match, strlist)
        return list(f)

class FileAnalize:
    def __init__(self, filename):
        self.filename = filename
        self.filetype = magic.from_file(self.filename, mime=False)
        if re.match('^PE', self.filetype) is not None:
            self.pe = PE(self.filename)
            with open(self.filename, 'rb') as alzfile:
                self.totalentropy = dataEntropy(alzfile.read())
                print self.totalentropy
        elif re.match('^ELF', self.filetype) is not None:
            self.elf = ELF(self.filename)
            with open(self.filename, 'rb') as alzfile:
                self.totalentropy = dataEntropy(alzfile.read())
        elif re.match('^Mach', self.filetype) is not None:
            self.macho = MachO(self.filename)
            with open(self.filename, 'rb') as alzfile:
                self.totalentropy = dataEntropy(alzfile.read())
        elif re.match('^MACH', self.filetype) is not None:
            self.macho = MachO(self.filename)
            with open(self.filename, 'rb') as alzfile:
                self.totalentropy = dataEntropy(alzfile.read())
        elif re.match('^OAT', self.filetype) is not None:
            self.oat = OAT(self.filename)
            with open(self.filename, 'rb') as alzfile:
                self.totalentropy = dataEntropy(alzfile.read())
        else:
            print 'ZOMG, filetype unknown ...\nI\'m currently only hacking through the following file types:\nELF\nPE\nMACH-O\nand\nOAT\nFor quick adoption of new file types, please add to filebytes github.com/sashs/filebytes\nThanks!'

    '''
    #检查文件编译时间
    Check File Compilation Time
    '''
    def checkFileDate(self):
        if re.match('^PE', self.filetype) is not None:
            pedate = self.pe.imageNtHeaders.header.FileHeader.TimeDateStamp
            filedate = int(time.ctime(pedate).split()[-1])
            return filedate
        elif re.match('^ELF', self.filetype) is not None:
            elfdate = os.path.getmtime(self.filename)
            filedate = int(time.ctime(elfdate).split()[-1])
            return filedate
        elif re.match('^Mach', self.filetype) is not None:
            machodate = os.path.getmtime(self.filename)
            filedate = int(time.ctime(machodate).split()[-1])
            return filedate
        elif re.match('^OAT', self.filetype) is not None:
            #oatdate = os.path.getmtime(self.filename)
            oat_dexdate = os.path.getmtime(self.filename)
            filedate = int(time.ctime(oat_dexdate).split()[-1])
            return filedate
        else:
            print 'ZOMG, filetype unknown ...\nI\'m currently only hacking through the following file types:\nELF\nPE\nMACH-O\nand\nOAT\nFor quick adoption of new file types, please add to filebytes github.com/sashs/filebytes\nThanks!'

    '''
    #查看运行平台
    View Running Platforms
    '''
    def checkMachine(self):
        if re.match('^PE', self.filetype) is not None:
            machine = self.pe.imageNtHeaders.header.FileHeader.Machine
            if 0x14c == machine:
                return 32
            elif 0x8664 == machine:
                return 64
            else:
                return -1
        elif re.match('^ELF', self.filetype) is not None:
            machine = hex(self.elf.elfHeader.header.e_machine)
            if 0x3 == machine:
                return x86
            elif 0x3E == machine:
                return x86-64
            elif 0x2 == machine:
                return SPARC
            elif 0x8 == machine:
                return MIPS
            elif 0x14 == machine:
                return PowerPC
            elif 0x28 == machine:
                return ARM
            elif 0x2A == machine:
                return SuperH
            elif 0x32 == machine:
                return IA-64
            elif 0xB7 == machine:
                return AArch64
            elif 0xF3 == machine:
                return RISC-V
            else:
                return -1
        elif re.match('^Mach', self.filetype) is not None:
            machine = hex(self.macho.machHeader.header.cputype)
            if 0x7 == machine:
                return x86-32
            elif 0x1000007L == machine:
                return x86-64
            else:
                return -1
        elif re.match('^OAT', self.filetype) is not None:
            machine = self.oat.oatDexHeader.Machine
            if 0x14c == machine:
                return 32
            elif 0x8664 == machine:
                return 64
            else:
                return -1
        else:
            print 'ZOMG, filetype unknown ...\nI\'m currently only hacking through the following file types:\nELF\nPE\nMACH-O\nand\nOAT\nFor quick adoption of new file types, please add to filebytes github.com/sashs/filebytes\nThanks!'

    '''
    #检查文件入口点
    Check File Entry Points
    '''
    def checkEntryPoint(self):
        if re.match('^PE', self.filetype) is not None:
            return hex(self.pe.entryPoint)
        elif re.match('^ELF', self.filetype) is not None:
            return hex(self.elf.entryPoint)
        elif re.match('^Mach', self.filetype) is not None:
            return hex(self.macho.entryPoint)
        elif re.match('^OAT', self.filetype) is not None:
            return hex(self.oat.entryPoint)
        else:
            print 'ZOMG, filetype unknown ...\nI\'m currently only hacking through the following file types:\nELF\nPE\nMACH-O\nand\nOAT\nFor quick adoption of new file types, please add to filebytes github.com/sashs/filebytes\nThanks!'

    '''
    #检查文件导入表内容
    Check File Import Table Contents
    #返回导入表{键-值}:{dll-API}
    Return Import Table {key-value}:{dll-API}
    '''
    def checkFileImports(self):
        if re.match('^PE', self.filetype) is not None:
            ret1 = [] # api信息/api Information
            ret2 = [] # alert信息/alert Information
            ret3 = {} # {dll-API}信息/{dll-API} Information
            if not self.pe.dataDirectory[ImageDirectoryEntry.IMPORT]:
                return ret1
            imports = self.pe.dataDirectory[ImageDirectoryEntry.IMPORT]
            if imports:
                for import_ in imports:
                    ret1 = []
                    for func in import_.importNameTable:
                        if func.importByName:
                            ret1.append(func.importByName.name)
                        ret3[import_.dllName] = ret1
            return ret3
        elif re.match('^ELF', self.filetype) is not None:
            ret1 = [] # api信息/api Information
            ret2 = [] # alert信息/alert Information
            #ret3 = {} # {dll-API}信息/{dll-API} Information
            lib = []
            for s in self.elf.sections:
                if re.match('^\.dyn', s.name):
                    if hasattr(s, 'content'):
                        for n in s.content:
                            if n.tag==1:
                                if n.val:
                                    lib.append(n.val)
                    elif hasattr(s, 'symbols'):
                        for n in s.symbols:
                            if n.header.st_shndx==0:
                                ret1.append(n.name)
            ret3 = dict.fromkeys(lib, 0)
            for k in ret3:
                ret3[k] = ret1
            return ret3
        elif re.match('^Mach', self.filetype) is not None:
            ret1 = [] # api信息/api Information
            ret2 = [] # alert信息/alert Information
            ret3 = {} # {dll-API}信息/{dll-API} Information
            if not hasattr(self.macho, 'LoadCommandData[name]'):
                return ret1
            for lib in self.macho.LoadCommandData[name]:
                for imp in lib.imports:
                    ret1.append(imp.name)
                ret3[lib.dll] = ret1
            return ret3
        elif re.match('^OAT', self.filetype) is not None:
            ret1 = [] # api信息/api Information
            ret2 = [] # alert信息/alert Information
            ret3 = {} # {dll-API}信息/{dll-API} Information
            if not hasattr(self.oat, 'DynamicData[header]'):
                return ret1
            for lib in self.oat.DynamicData[header]:
                for imp in lib.imports:
                    ret1.append(imp.name)
                ret3[lib.dll] = ret1
            return ret3
        else:
            print 'ZOMG, filetype unknown ...\nI\'m currently only hacking through the following file types:\nELF\nPE\nMACH-O\nand\nOAT\nFor quick adoption of new file types, please add to filebytes github.com/sashs/filebytes\nThanks!'

    '''
    #检查pe文件节信息
    Check PE File Section Information
    '''
    def checkFileSections(self):
        # 立两个flag/Stand Two Flag
        entropyflag  = False
        datasizeflag = False
        # 储存变量的list/Stored Variables list
        virtualSize  = []
        pefileinfos  = []
        elffileinfos  = []
        machfileinfos  = []
        oatfileinfos  = []
        if re.match('^PE', self.filetype) is not None:
            # 获取文件节个数/Get the Number of File Sections
            numofsection = self.pe.imageNtHeaders.header.FileHeader.NumberOfSections
            pefileinfos.append(numofsection)
            for section in self.pe.sections:
                entropy = dataEntropy(section.bytes)
                pefileinfos.append(section.header.Name.strip(b"\x00").decode(errors='ignore'))
                pefileinfos.append(hex(section.header.VirtualAddress))
                pefileinfos.append(section.header.PhysicalAddress_or_VirtualSize)
                pefileinfos.append(section.header.SizeOfRawData)
                pefileinfos.append(str(entropy))
            return pefileinfos
        elif re.match('^ELF', self.filetype) is not None:
            # 获取文件节个数/Get the Number of File Sections
            numofsection = len(self.elf.sections)
            elffileinfos.append(numofsection)
            for section in self.elf.sections:
                try:
                    entropy = dataEntropy(section.bytes)
                except:
                    entropy = 0
                elffileinfos.append(section.name)
                elffileinfos.append(section.header.sh_addr)
                elffileinfos.append(section.header.sh_offset)
                elffileinfos.append(section.header.sh_size)
                elffileinfos.append(str(entropy))
            return elffileinfos
        elif re.match('^Mach', self.filetype) is not None:
            # 获取文件节个数/Get the Number of File Sections
            machfileinfos = []
            numofsection = 0
            for entry in self.macho.loadCommands:
                try:
                    numofsection = numofsection + len(entry.sections)
                except:
                    pass
            machfileinfos.append(numofsection)
            for entry in self.macho.loadCommands:
                try:
                    for section in entry.sections:
                        entropy = dataEntropy(section.bytes)
                        n = section.name.replace('__','.')
                        machfileinfos.append(n)
                        r = str(section.header)
                        f = r[r.find('0x'):]
                        c = f.strip('>')
                        machfileinfos.append(c)
                        machfileinfos.append(len(section.bytes))
                        machfileinfos.append(len(section.raw))
                        machfileinfos.append(str(entropy))
                except:
                    pass
            return machfileinfos
        elif re.match('^OAT', self.filetype) is not None:
            # 获取文件节个数/Get the Number of File Sections
            numofsection = self.oat.elfHeader.NumberOfSections
            oatfileinfos.append(numofsection)
            for section in self.oat.sections:
                entropy = section.get_entropy()
                oatfileinfos.append(section.Name.strip(b"\x00").decode(errors='ignore'))
                oatfileinfos.append(hex(section.VirtualAddress))
                oatfileinfos.append(section.Misc_VirtualSize)
                oatfileinfos.append(section.SizeOfRawData)
                oatfileinfos.append(str(entropy))
            return oatfileinfos
        else:
            print 'ZOMG, filetype unknown ...\nI\'m currently only hacking through the following file types:\nELF\nPE\nMACH-O\nand\nOAT\nFor quick adoption of new file types, please add to filebytes github.com/sashs/filebytes\nThanks!'

    def checkFileHeader(self):
        debugflag      = False # 包含调试信息/Include Debugging Information
        suspiciousflag = False # 可疑标志/Suspicious Flags
        if re.match('^PE', self.filetype) is not None:
            if self.pe.imageNtHeaders.header.FileHeader.PointerToSymbolTable > 0:
                debugflag = True

            flags = [("BYTES_REVERSED_LO", self.pe.imageDosHeader.IMAGE_FILE_BYTES_REVERSED_LO,
                      "Little endian: LSB precedes MSB in memory, deprecated and should be zero."),
                     ("BYTES_REVERSED_HI", self.pe.imageDosHeader.IMAGE_FILE_BYTES_REVERSED_HI,
                      "Big endian: MSB precedes LSB in memory, deprecated and should be zero."),
                     ("RELOCS_STRIPPED", self.pe.imageDosHeader.IMAGE_FILE_RELOCS_STRIPPED,
                      "This indicates that the file does not contain base relocations and must therefore be loaded at its preferred base address.\nFlag has the effect of disabling Address Space Layout Randomization(ASPR) for the process.")]
            if any(tr[1] for tr in flags):
                sussuspiciousflag = True
                for n in flags:
                    if n[1]:
                        print n[0] + "Flag is Set - {}".format(n[2])

        elif re.match('^ELF', self.filetype) is not None:
            if self.pe.elfHeader.PointerToSymbolTable > 0:
                debugflag = True

            flags = [("BYTES_REVERSED_LO", self.pe.elfHeader.IMAGE_FILE_BYTES_REVERSED_LO,
                      "Little endian: LSB precedes MSB in memory, deprecated and should be zero."),
                     ("BYTES_REVERSED_HI", self.pe.elfHeader.IMAGE_FILE_BYTES_REVERSED_HI,
                      "Big endian: MSB precedes LSB in memory, deprecated and should be zero."),
                     ("RELOCS_STRIPPED", self.pe.elfHeader.IMAGE_FILE_RELOCS_STRIPPED,
                      "This indicates that the file does not contain base relocations and must therefore be loaded at its preferred base address.\nFlag has the effect of disabling Address Space Layout Randomization(ASPR) for the process.")]
            if any(tr[1] for tr in flags):
                sussuspiciousflag = True
                for n in flags:
                    if n[1]:
                        print n[0] + "Flag is Set - {}".format(n[2])

        elif re.match('^MACH', self.filetype) is not None:
            if self.pe.machHeader.PointerToSymbolTable > 0:
                debugflag = True

            flags = [("BYTES_REVERSED_LO", self.pe.machHeader.IMAGE_FILE_BYTES_REVERSED_LO,
                      "Little endian: LSB precedes MSB in memory, deprecated and should be zero."),
                     ("BYTES_REVERSED_HI", self.pe.machHeader.IMAGE_FILE_BYTES_REVERSED_HI,
                      "Big endian: MSB precedes LSB in memory, deprecated and should be zero."),
                     ("RELOCS_STRIPPED", self.pe.machHeader.IMAGE_FILE_RELOCS_STRIPPED,
                      "This indicates that the file does not contain base relocations and must therefore be loaded at its preferred base address.\nFlag has the effect of disabling Address Space Layout Randomization(ASPR) for the process.")]
            if any(tr[1] for tr in flags):
                sussuspiciousflag = True
                for n in flags:
                    if n[1]:
                        print n[0] + "Flag is Set - {}".format(n[2])

        elif re.match('^OAT', self.filetype) is not None:
            if self.pe.oatHeader.PointerToSymbolTable > 0:
                debugflag = True

            flags = [("BYTES_REVERSED_LO", self.pe.oatHeader.IMAGE_FILE_BYTES_REVERSED_LO,
                      "Little endian: LSB precedes MSB in memory, deprecated and should be zero."),
                     ("BYTES_REVERSED_HI", self.pe.oatHeader.IMAGE_FILE_BYTES_REVERSED_HI,
                      "Big endian: MSB precedes LSB in memory, deprecated and should be zero."),
                     ("RELOCS_STRIPPED", self.pe.oatHeader.IMAGE_FILE_RELOCS_STRIPPED,
                      "This indicates that the file does not contain base relocations and must therefore be loaded at its preferred base address.\nFlag has the effect of disabling Address Space Layout Randomization(ASPR) for the process.")]
            if any(tr[1] for tr in flags):
                sussuspiciousflag = True
                for n in flags:
                    if n[1]:
                        print n[0] + "Flag is Set - {}".format(n[2])

        else:
            print 'ZOMG, filetype unknown ...\nI\'m currently only hacking through the following file types:\nELF\nPE\nMACH-O\nand\nOAT\nFor quick adoption of new file types, please add to filebytes github.com/sashs/filebytes\nThanks!'

class DefaultAnalyze(QtCore.QThread):
    numberSignal = QtCore.pyqtSignal(int, str)
    valueSignal  = QtCore.pyqtSignal(int, str)

    def __init__(self, filename, md5, index, parent=None):
        super(DefaultAnalyze, self).__init__(parent)
        self.filename  = filename
        self.md5       = md5
        self.Analize = FileAnalize(self.filename)

    # PE文件分析测试函数/PE File Analysis Test Function
    def test(self):
        Analize = FileAnalize(self.filename)
        Analize.checkEntryPoint()
        Analize.checkFileDate()
        Analize.checkMachine()
        # Analize.checkFileHeader()
        Analize.checkFileImports()
        Analize.checkFileSections()

    def func1(self, q):
        result1 = self.Analize.checkFileDate()
        result2 = self.Analize.checkEntryPoint()
        result3 = self.Analize.checkMachine()
        q.put((1, result1, result2, result3))

    def func2(self, q):
        result = self.Analize.checkFileImports()
        q.put((2, result))

    def func3(self, q):
        result = self.Analize.checkFileSections()
        q.put((3, result))

    # python threading模块测试函数/Python threading Module Test Function
    # 三个子函数时比顺序执行平均快3秒/Three Sub Functions are Performed on Average 3 Seconds Faster than Sequential Execution
    def PEThreadControl(self, q):
        tlist = []
        t1 = threading.Thread(target=self.func1, args=(q,))
        tlist.append(t1)
        t2 = threading.Thread(target=self.func2, args=(q,))
        tlist.append(t2)
        t3 = threading.Thread(target=self.func3, args=(q,))
        tlist.append(t3)
        for i in tlist:
            i.start()
        for i in tlist:
            i.join()

    '''
    #写入PE文件信息
    Write to PE File Information
    #md5:文件md5值，作为数据库外键
    MD5: File MD5 Value, as a Database Foreign Key
    #queue:PE分析线程队列
    queue:PE Profiling Thread Queues
    #return数据库执行结果
    Return Database Execution Results
    #-1:数据库连接失败
    -1: Database Connection Failed
    #-2:更新数据失败
    -2: Failed to Update Data
    # 1:数据库更新成功
     1: Database Update Succeeded
    '''
    def write2PEInfoDB(self, md5, queue):
        try:
            sqlconn = sqlite3.connect('../db/fileinfo.db')
        except sqlite3.Error, e:
            print "sqlite connect failed", "\n", e.args[0]
            return -1
        sqlcursor = sqlconn.cursor()
        try:
            print "insert a new pe file info"
            sqlcursor.execute("insert into pe_info (md5) values(?)", (md5,))
            while(not queue.empty()):
                info = queue.get()
                if 1 == info[0]:
                    # print info[1], info[2]
                    sqlcursor.execute("update pe_info set cpltime=?, entrypnt=?, petype=? where md5=?", (info[1], info[2], info[3], md5))
                elif 2 == info[0]:
                    # print info[1]
                    sqlcursor.execute("update pe_info set impinfo=? where md5=?", (str(info[1]), md5))
                else:
                    # print info[1]
                    sqlcursor.execute("update pe_info set setinfo=? where md5=?", (str(info[1]), md5))
            sqlconn.commit()
            sqlconn.close()
            return 1
        except sqlite3.Error, e:
            print "Error Reading DB Data!", "\n", e.args[0]
            return -2

    def run(self):
        print "run function in defaultanalyze class"
        # self.test()
        que = Queue.Queue()
        self.PEThreadControl(que)
        ret = self.write2PEInfoDB(self.md5, que)
        self.valueSignal.emit(ret, self.md5)
