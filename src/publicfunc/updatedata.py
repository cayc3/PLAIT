#coding=utf-8

from PyQt5 import QtCore
import os, sys, shutil
import urllib
import git

class UpdateData(QtCore.QObject):

    def __init__(self, parent=None):
        QtCore.QObject.__init__(self)

    '''
    #从github下载App规则库库
    Update from GitHub
    '''
    def pullApp(self):
	try:
            print "Updating Analysis Tool ..."
            DIR_NAME = '..\/'
            REMOTE_URL = 'https://github.com/zengrx/S.M.A.R.T'
            repo = git.Repo.init(DIR_NAME)
            origin = repo.create_remote('origin',REMOTE_URL)
            origin.fetch()
            origin.pull(origin.refs[0].remote_head)
            #git.Git().pull('https://github.com/zengrx/S.M.A.R.T', '../')
            print "Updated"
            return
        except:
            print "Update Failed"
    '''
    #从github下载yara规则库库
    Download Yara Rule Library from GitHub
    '''
    def cloneYaraData(self):
        if not os.path.exists("rules"):
            os.mkdir("rules")
        if not os.path.exists("rules_compiled"):
            os.mkdir("rules_compiled")
        if not os.listdir("rules"):
            print "Downloading Yara-Rules ..."
            git.Git().clone("https://github.com/Yara-Rules/rules")
            print "Got Yara Rules"
            return
        else:
            print "Yara Data is Present"

    '''
    #更新yara更新库
    Update Yara Update Library
    '''
    def updateYaraData(self):
        #print u"更新规则库"
        print u"Updating the Rule Library ..."
        import time
        time.sleep(10)
        if os.path.exists("rules"):
            shutil.rmtree("rules")
        if os.path.exists("rules_compiled"):
            shutil.rmtree("rules_compiled")
        #os.mkdir("rules_compiled")
        self.cloneYaraData()
        print "Yara Data Updated."
        return

    '''
    #从github下载yara规则库库
    Download Clam Definitions
    '''
    def cloneClamData(self):
        if not os.path.exists("clam"):
            os.mkdir("clam")
        #if not os.path.exists("rules_compiled"):
        #    os.mkdir("rules_compiled")
        #if not os.listdir("clam"):
	print "Downloading ClamAV-Definitions ..."
	if os.path.exists('clam/main.cvd') is False:
		urllib.urlretrieve('http://database.clamav.net/main.cvd', 'clam/main.cvd')
		print 'Got Main Defs'
	if os.path.exists('clam/bytecode.cvd') is False:
		urllib.urlretrieve('http://database.clamav.net/bytecode.cvd', 'clam/bytecode.cvd')
		print 'Got Bytecode Defs'
	if os.path.exists('clam/daily.cvd') is False:
		urllib.urlretrieve('http://database.clamav.net/daily.cvd', 'clam/daily.cvd')
		print 'Got Latest Defs'
		return
	else:
		print "Clam Data is Present. Checking for Updates ..."

    '''
    #更新yara更新库
    Update Clam Definitions
    '''
    #def updateClamData(self):
        #print u"更新规则库"
        #print u"Updating Clam Definitions ..."
        #import time
        #time.sleep(10)
        #if os.path.exists("rules"):
        #    shutil.rmtree("rules")
        #if os.path.exists("rules_compiled"):
        #    shutil.rmtree("rules_compiled")
        #os.mkdir("rules_compiled")
        #self.cloneYaraData()
        #print "Clam Data Updated."
        #return
