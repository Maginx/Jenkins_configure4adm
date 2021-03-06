﻿from modules.jenkins import Jenkins

class AdmJenkins(Jenkins):
    ''' Configure jenkins job class
    '''
    __NO_MAN_PAGE = '''scm/excludedRegions==%(commonpart)so2ml/content/*.man
%(commonpart)so2ml/content/amanual/*.man,scm/includedRegions==%(commonpart)so2ml/content/.*
%(commonpart)srobot/src/.*
%(commonpart)srobot/robotsources.xml,publishers/hudson.tasks.junit.JUnitResultArchiver/testResults==TEST-unittest.suite.TestSuite.xml,builders/hudson.tasks.Shell/command==echo \"mpp_build_type=o2ml\" > build-type.conf;'''
    __MAN_PAGE = '''scm/excludedRegions==,scm/includedRegions==%(commonpart)so2ml/content/*.man
%(commonpart)so2ml/content/amanual/*.man,role==hudson.model.Item.Read:I_EXT_TERMINATORS,role==hudson.model.Item.Workspace:I_EXT_TERMINATORS,role==hudson.model.Item.Build:I_EXT_TERMINATORS,role==hudson.model.Item.Configure:I_EXT_TERMINATORS,publishers/hudson.plugins.robot.RobotPublisher==,publishers/hudson.tasks.junit.JUnitResultArchiver/testResults==TEST-unittest.suite.TestSuite.xml,builders/hudson.tasks.Shell/command==echo \"mpp_build_type=man\" > build-type.conf;'''
    __JENKINS_BRANCH_FORMAT = "adaptation_branch_%(branchName)s_%(releaseId)s_ris"
    __JENKINS_TRUNK_FORMAT = "adaptation_trunk_%(releaseId)s_ris"

    def __init__(self, url, user, password):
        ''' Initial necessary message
        @param url : jenkins url path, string
        @param user : jenkins user , string
        @param password : corresponding password, string
        '''
        if not url:
            url = "https://eslinv70.emea.nsn-net.net:8080"
        if not user:
            user = "j69wang"
        if not password:
            password = "PAssword123"
        super(AdmJenkins, self).__init__(url, user, password)
        
    def get_job_releaseid(self, releaseId):
        ''' Get jenkisn job name by release id
        @param releaseId  : release id, string
        @return : jenkins job name
        @exception : NullException
        '''
        releaseId = self.__filter_release_id(releaseId)
        if not releaseId:
            TraceLog.warn("release id is incorrect [%s]" % releaseId)
        jobname = self.__JENKINS_TRUNK_FORMAT % locals()
        if not self.job_exists(jobname):
            return None
        return jobname
     
    def __filter_release_id(self, releaseId):
        '''Convert full release id to short name
        @param releaseId : full release id, string
        @return releaseId : shot release id, string
        '''
        if "com.nsn." in releaseId:
            return releaseId.split('com.nsn.')[-1]
        if "com.nokia." in releaseId:
            return releaseId.split('com.nokia.')[-1]
        if "com.nokianetworks." in releaseId:
            return releaseId.split('com.nokianetworks.')[-1]
        return releaseId

    def get_job_branch_releaseid(self, branchName, releaseId):
        '''Get jenkins job name by branch name and release id
        @param branchName : branch name, string
        @param releaseId  : release id, string
        '''
        if not branchName or not releaseId:
            return EmptyException("release id or branch name is incorrect %s %s" % (branchName,releaseId))
        jobname = self.__JENKINS_BRANCH_FORMAT % locals()
        if self.job_exists(jobname):
            return jobname
        return self.__seek_job(branchName, releaseId)
    
    def __seek_job(self, branchName, releaseId):
        '''Seek the job name based on persent jenkins job format
        @param branchName : branch name, string
        @param releaseId  : component release id,string
        @exception NullException : can't find out the correct jenkins job name
        @return jobname : jenkins job name ,string
        '''
        jobname = JENKINS_BRANCH_FORMAT % locals()
        if self.job_exists(jobname):
            return jobname;
        if releaseId.startwith("com.nsn."):
            releaseId = releaseId.split('com.nsn.')[-1]
            jobname = JENKINS_BRANCH_FORMAT % locals()
            if self.job_exists(jobname):
                return jobname
        if releaseId.startwith("com.nokia."):
            releaseId = releaseId.split('com.nokia.')[-1]
            jobname = JENKINS_BRANCH_FORMAT % locals()
            if self.job_exists(job_name):
                return jobanme
        if releaseId.startwith("com.nokianetworks."):
            releaseId = releaseId.split('com.nokianetworks.')[-1]
            jobname = JENKINS_BRANCH_FORMAT % locals()
            if self.job_exists(job_name):
                return jobanme
        return NullException("can't find the jenkins job name %s %s" % (branchName,releaseId))

    def get_man_job(self, jobName):
        ''' Generate the man page jenkins job name by exsting jenkins job
        @param jobName : jenkins job name, string
        @return : man page jenkins job name, string
        @exception : EmptyException
        '''
        if not jobName.strip():
            return None
        parts = jobName.rsplit('-',1)
        return ".man-".join(parts)
        
    def config_job(self, jobName, commonpart):
        '''Configure jenkins job
        @param jobName : jenkins job name, string
        @param commonpart : common part to config, string
        @return: new configure file
        @exception : XmlException, Exception
        '''
        pairs = self.__NO_MAN_PAGE % locals()
        if not self.job_exists(jobName):
            TraceLog.warning("jenkins job name does not exist [%s]" % jobName)
            return False
        configure = self.get_job_xml(jobName)
        manjob = self.get_man_job(jobName)
        if not FileHandler.copyfile(configure,"%s.xml" % manjob):
            TraceLog.warning("copy file from [%s] to [%s]" , (configure, "%s.xml" % manjob))
            return False
        try:
            self.__modify_xml(pairs,configure)
            if not self.reconfig_job(jobName,configure):
                return False
        except Exception,e:
            TraceLog.error(e)
            return False
        return True

    def __modify_xml(self, pairs, xmlfile):
        '''Modify xml file 
        @param pairs    : key=value parameters, string
        @param xmlfile  : configure xml file path
        '''
        for pair in pairs.strip().split(','):
            if not ConfigureJenkins.reconfigjenkins(pair.split('==')[0], pair.split('==')[1], xmlfile):
                print("config jenkins job configure file failed to %s" % pair)

    def create_job(self, jobName, commonpart):
        '''Create jenkins job
        @param jobName      : jenkins job name,string
        @param commonpart   : common part to configure, string
        '''
        if self.job_exists(jobName):
            TraceLog.warning("jenkins job alredy exist [%s]" % jobName)
            return True
        pairs = self.__MAN_PAGE % locals() 
        destfile = "%s.xml" % jobName
        try:
            self.__modify_xml(pairs,destfile)
            return super(AdmJenkins, self).create_job(jobName,destfile)
        except  JenkinsException, e:
            TraceLog.error(e)
            return False

    def get_svnurl(self, jobName):
        '''Get jenkins job svn url from configure
        @param jobName : jenkins job name
        @return svnpath : jenkins job corresponding svn path
        '''
        xml_content = self.get_job_xml(jobName)
        if not xml_content:
            return None
        return ConfigureJenkins.get_config_jenkins("scm/locations/hudson.scm.SubversionSCM_-ModuleLocation/remote",xml_content)
if __name__ == "__main__":
    print("jenkins")