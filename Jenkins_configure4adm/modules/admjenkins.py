from modules.logger import TraceLog
from modules.jenkins import Jenkins
from modules.configurejenkins import ConfigureJenkins
from modules.filehandler import FileHandler
from modules.errors import JenkinsException, EmptyException, NullException

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

    def get_job_releaseid(self, release_id):
        ''' Get jenkisn job name by release id
        @param release_id  : release id, string
        @return : jenkins job name
        @exception : NullException
        '''
        release_id = self.__filter_release_id(release_id)
        if not release_id:
            TraceLog.warning("release id is incorrect [%s]" % release_id)
        jobname = self.__JENKINS_TRUNK_FORMAT % locals()
        if not self.job_exists(jobname):
            return None
        return jobname

    def __filter_release_id(self, release_id):
        '''Convert full release id to short name
        @param release_id : full release id, string
        @return releaseId : shot release id, string
        '''
        if "com.nsn." in release_id:
            return release_id.split('com.nsn.')[-1]
        if "com.nokia." in release_id:
            return release_id.split('com.nokia.')[-1]
        if "com.nokianetworks." in release_id:
            return release_id.split('com.nokianetworks.')[-1]
        return release_id

    def get_job_branch_releaseid(self, branch_name, release_id):
        '''Get jenkins job name by branch name and release id
        @param branch_name : branch name, string
        @param release_id  : release id, string
        '''
        if not branch_name or not release_id:
            return EmptyException("release id or branch name is incorrect "
                                  + branch_name + release_id)
        job_name = self.__JENKINS_BRANCH_FORMAT % locals()
        if self.job_exists(job_name):
            return job_name
        return self.__seek_job(branch_name, release_id)

    def __seek_job(self, branch_name, release_id):
        '''Seek the job name based on persent jenkins job format
        @param branch_name : branch name, string
        @param release_id  : component release id,string
        @exception NullException : can't find out the correct jenkins job name
        @return jobname : jenkins job name ,string
        '''
        job_name = self.__JENKINS_BRANCH_FORMAT % locals()
        if self.job_exists(job_name):
            return job_name
        if release_id.startwith("com.nsn."):
            release_id = release_id.split('com.nsn.')[-1]
            job_name = self.__JENKINS_BRANCH_FORMAT % locals()
            if self.job_exists(job_name):
                return job_name
        if release_id.startwith("com.nokia."):
            release_id = release_id.split('com.nokia.')[-1]
            job_name = self.__JENKINS_BRANCH_FORMAT % locals()
            if self.job_exists(job_name):
                return job_name
        if release_id.startwith("com.nokianetworks."):
            release_id = release_id.split('com.nokianetworks.')[-1]
            job_name = self.__JENKINS_BRANCH_FORMAT % locals()
            if self.job_exists(job_name):
                return job_name
        return NullException("can't find the jenkins job name %s %s" % (branch_name, release_id))

    def get_man_job(self, job_name):
        ''' Generate the man page jenkins job name by exsting jenkins job
        @param job_name : jenkins job name, string
        @return : man page jenkins job name, string
        @exception : EmptyException
        '''
        if not job_name.strip():
            return None
        parts = job_name.rsplit('-', 1)
        man_job = ".man-".join(parts)
        return man_job

    def config_job(self, job_name):
        '''Configure jenkins job
        @param job_name : jenkins job name, string
        @return: new configure file
        @exception : XmlException, Exception
        '''
        pairs = self.__NO_MAN_PAGE % locals()
        file_name = self.get_job_xml_filepath(job_name)
        man_job = self.get_man_job(job_name)
        if not FileHandler.copyfile(file, "%s.xml" % man_job):
            TraceLog.warning("copy file from [%s] to [%s] ", (file_name, "%s.xml" % man_job))
            return False
        try:
            self.__modify_xml(pairs, file)
            if not self.reconfig_job(job_name, file_name):
                return False
        except Exception as exc:
            TraceLog.error(exc)
            return False
        finally:
            FileHandler.delete_temp_file(file_name)
        return True

    def __modify_xml(self, pairs, xmlfile):
        '''Modify xml file
        @param pairs    : key=value parameters, string
        @param xmlfile  : configure xml file path
        '''
        for pair in pairs.strip().split(','):
            if not ConfigureJenkins.reconfig_jenkins(pair.split('==')[0], pair.split('==')[1], xmlfile):
                TraceLog.info("config jenkins job configure file failed to %s" % pair)

    def create_job(self, job_name):
        '''Create jenkins job
        @param job_name      : jenkins job name,string
        '''
        pairs = self.__MAN_PAGE % locals() 
        dest_file = "%s.xml" % job_name
        try:
            self.__modify_xml(pairs, dest_file)
            return super(AdmJenkins, self).create_job(job_name, dest_file)
        except  JenkinsException as exception:
            TraceLog.error(exception)
            return False

    def get_svn_url(self, job_name):
        '''Get jenkins job svn url from configure
        @param job_name : jenkins job name
        @return svn_path : jenkins job corresponding svn path
        '''
        TraceLog.info("get jenkins job svn path")
        xmlfile_name = self.get_job_xml_filepath(job_name)
        if not xmlfile_name:
            return None
        result = ConfigureJenkins.get_config_jenkins("scm/locations/hudson.scm.SubversionSCM_-ModuleLocation/remote",xmlfile_name)
        if not result:
            FileHandler.delete_temp_file(xmlfile_name)
            return None
        return result        
    
if __name__ == "__main__":
    adm_jenkins = AdmJenkins(url=None, user=None, password=None)
