import sys
import io
from mimify import File
import os
sys.path.append(sys.path.append(sys.path[0].split('modules')[-2]))
from modules.errors import XmlException
from modules.xmlconfigure import ConfigParser

class ConfigureJenkins(ConfigParser):
    '''Config jenkins job configure file
    '''
    config = None

    @classmethod
    def reconfig_jenkins(cls, configtagname, value, sourcefile):
        '''Reconfig jenkins job configuration
        @param configTagname : config xml tag 
        @param value         : corresponding value
        @param sourceFile    : source xml file
        '''
        config = ConfigParser(sourcefile,sourcefile)
        try:
            if configtagname == "role":
                config.add_node("properties/hudson.security.AuthorizationMatrixProperty","permission",value)
            elif configtagname == "builders/hudson.tasks.Shell/command":
                config.add_value("builders/hudson.tasks.Shell/command", value)
            else:
                config.modify_value(configtagname,value)
            return True
        except  XmlException,e:
            print(e.message)
            return False

    @classmethod
    def get_config_jenkins(cls, path,sourcefile):
        '''Get jenkins corresponding node value
        @param path : jenkins path name, string
        @param sourcefile : source file path, string
        '''
        return ConfigParser(sourcefile).get_node_value(path)

    
if __name__ == "__main__" : 
    content = "D:\userdata\j69wang\Desktop\config.xml"
    ConfigureJenkins.get_config_jenkins("scm/locations/hudson.scm.SubversionSCM_-ModuleLocation/remote",content)
    ConfigureJenkins.reconfig_jenkins('role','j20li',content)
    ConfigureJenkins.reconfig_jenkins('builders/hudson.tasks.Shell/command','Test',content)
    ConfigureJenkins.reconfig_jenkins('publishers/hudson.tasks.junit.JUnitResultArchiver/testResults','TEST-unittest.suite.TestSuite.xml',content)
    
