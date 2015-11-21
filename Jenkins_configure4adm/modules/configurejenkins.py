# -*- coding: UTF-8 -*-
from modules.xmlconfigure import ConfigParser
from modules.errors import XmlException

class ConfigureJenkins(ConfigParser):
    '''Config jenkins job configure file
    '''
    config = None

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
    
    def get_config_jenkins(cls, path,sourcefile):
        '''Get jenkins corresponding node value
        @param path : jenkins path name, string
        @param sourcefile : source file path, string
        '''
        config = ConfigParser(sourcefile,sourcefile)
        return ConfigParser(sourcefile,sourcefile).get_node_value(path)