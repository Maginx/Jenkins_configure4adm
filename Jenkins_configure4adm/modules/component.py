# -*- coding: UTF-8 -*-
import re
from modules.shell import run_shell

class AdapComponent(object):
    '''Adaptation component class
    '''
    __COMMON_PART = "/%(branchname)s/%(adapid)s/%(adaprelease)s/"

    def __init__(self,path):
        '''Initial class instance
        @param path : adaptation component path
        '''
        self.svnpath = path

    def parse_svn_path(self):
        '''Parse svn path by split key word
        @return : adapid adaptation id, string
        @return : adapreleae adaptation release, string
        '''
        return self.truncate_svnpath(-2),self.truncate_svnpath(-1)
    
    def truncate_svnpath(self, index):
        '''Truncate the string by index to get adaptation details
        @param content : partly svn path string ,e.g. {branch name}/{adaptation id}/{adaptation release}, string
        @param index  : svn path part index
        @return partconent, string
        '''
        if not self.svnpath:
            return ValueError("Truncate svn path error: string is empty content %s " % content)
        adaps = self.svnpath.strip('/').split('/')
        try:
            return adaps[index]
        except IndexError, e:
            print("Index error %s " % e)
            return None
    
    def get_common_part(self):
        '''Get the common part(include/exclude)
        @return common part, string
        '''
        adapid, adaprelease = self.parse_svn_path()
        branchname = "%(branchname)s"
        return self.__COMMON_PART % locals()
    
    def exist_manpom(self):
        '''Verify the pom_man.xml exist or not?
        '''
        retcode, stdout, stderr = run_shell("svn ls %s" % self.svnpath,True)
        if stdout.__contains__("pom_man.xml"):
            return True
        else:
            print("[%s] pom_man.xml doesn't exist" % self.svnpath)
            return False

class BranchComponent(AdapComponent):
    '''Branch adaptation component class
    '''
    def __init__(self, path):
        return super(BranchComponent, self).__init__(path)

    def parse_svn_path(self, splitchar):
        '''Parse svn path to get adaptation details
        @param splitchar : split char key word, string
        @return adapid : adaptation id, string
        @return adaprelease : adaptation release, string
        @return branch name : branch name, string
        @exception : ValueError
        '''
        adapid,adaprelease = super(BranchComponent, self).parse_svn_path(splitchar)
        branchname = self.truncate_svnpath(-3)
        return adapid, adaprelease, branchname

    def get_common_part(self):
        '''Get the common part(include/exclude)
        @return common part, string
        '''
        branchname = self.truncate_svnpath(-3)
        return super(BranchComponent, self).get_common_part() % locals()

class TrunkComponent(AdapComponent):
    ''' Trunk adaptation component 
    '''
    def __init__(self, path):
        '''Initial trunk component 
        @param path : trunk component path
        '''
        return super(TrunkComponent, self).__init__(path)

    def parse_svn_path(self):
        '''Parse svn path to get adaptation details
        @return adapid : adaptation id, string
        @return adaprelease : adaptation release, string
        @exception ValueError
        '''
        return super(TrunkComponent, self).parse_svn_path()
    
    def get_common_part(self):
        '''Get common part (include/exclude)
        @return common part, string
        '''
        branchname = "trunk"
        return super(TrunkComponent, self).get_common_part() % locals()