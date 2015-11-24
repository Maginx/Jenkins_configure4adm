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
        temp = "temp.xml"
        config = ConfigParser(ConfigureJenkins.__create_file(temp,sourcefile))
        result = ConfigParser(config).get_node_value()
        ConfigureJenkins.__delete_file(temp)
        return result
    
    @classmethod
    def __create_file(cls, name, content):
        with open(name, 'wt') as f:
            f.write(content)
        return name

    @classmethod
    def __delete_file(cls, name):
       os.remove(name)
    
if __name__ == "__main__" : 
    cotnent = '''<project><actions/><description>Adaptations are built with maven and tested on backend with robotframework.</description><logRotator class="hudson.tasks.LogRotator"><daysToKeep>60</daysToKeep><numToKeep>10</numToKeep><artifactDaysToKeep>10</artifactDaysToKeep>
<artifactNumToKeep>10</artifactNumToKeep>
</logRotator>
<keepDependencies>false</keepDependencies>
<properties>
<hudson.security.AuthorizationMatrixProperty>
<permission>hudson.model.Item.Delete:j69wang</permission>
<permission>hudson.model.Item.Read:j69wang</permission>
<permission>hudson.model.Item.Workspace:j69wang</permission>
<permission>hudson.model.Item.Build:j69wang</permission>
<permission>hudson.model.Item.Configure:j69wang</permission>
<permission>
hudson.model.Item.Configure:I_EXT_MPP_SCM_ADAPTATIONS_VS_KU
</permission>
</hudson.security.AuthorizationMatrixProperty>
<hudson.plugins.throttleconcurrents.ThrottleJobProperty plugin="throttle-concurrents@1.8.4">
<maxConcurrentPerNode>0</maxConcurrentPerNode>
<maxConcurrentTotal>0</maxConcurrentTotal>
<throttleEnabled>false</throttleEnabled>
<throttleOption>project</throttleOption>
</hudson.plugins.throttleconcurrents.ThrottleJobProperty>
</properties>
<scm class="hudson.scm.SubversionSCM" plugin="subversion@2.4.5">
<locations>
<hudson.scm.SubversionSCM_-ModuleLocation>
<remote>
https://svne1.access.nokiasiemensnetworks.com/isource/svnroot/adaptations/trunk/NOKGGSN/NOKGGSN-FI5.0
</remote>
<credentialsId>0df61b7c-4d3f-4db0-ae8b-c9f9a33f4bd1</credentialsId>
<local>.</local>
<depthOption>infinity</depthOption>
<ignoreExternalsOption>false</ignoreExternalsOption>
</hudson.scm.SubversionSCM_-ModuleLocation>
</locations>
<browser class="hudson.scm.browsers.Assembla">
<spaceName/>
</browser>
<excludedRegions></excludedRegions>
<includedRegions/>
<excludedUsers/>
<excludedRevprop/>
<excludedCommitMessages/>
<workspaceUpdater class="hudson.scm.subversion.UpdateUpdater"/>
<ignoreDirPropChanges>false</ignoreDirPropChanges>
<filterChangelog>false</filterChangelog>
</scm>
<assignedNode>rhel6</assignedNode>
<canRoam>false</canRoam>
<disabled>false</disabled>
<blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
<blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
<triggers>
<hudson.triggers.SCMTrigger>
<spec>0 0 1 1 *</spec>
<ignorePostCommitHooks>false</ignorePostCommitHooks>
</hudson.triggers.SCMTrigger>
</triggers>
<concurrentBuild>false</concurrentBuild>
<builders>
<hudson.tasks.Shell>
<command>
env echo "build.number=$BUILD_NUMBER" > build-number.txt .mpp/build
</command>
</hudson.tasks.Shell>
</builders>
<publishers>
<hudson.tasks.junit.JUnitResultArchiver plugin="junit@1.5">
<testResults>o2ml/TEST-unittest.suite.TestSuite.xml</testResults>
<keepLongStdio>false</keepLongStdio>
<healthScaleFactor>1.0</healthScaleFactor>
</hudson.tasks.junit.JUnitResultArchiver>
<hudson.plugins.robot.RobotPublisher plugin="robot@1.6.0">
<outputPath>robot-log/</outputPath>
<reportFileName>report.html</reportFileName>
<logFileName>log.html</logFileName>
<outputFileName>output.xml</outputFileName>
<disableArchiveOutput>false</disableArchiveOutput>
<passThreshold>100.0</passThreshold>
<unstableThreshold>100.0</unstableThreshold>
<otherFiles>
<string/>
</otherFiles>
<onlyCritical>true</onlyCritical>
</hudson.plugins.robot.RobotPublisher>
<hudson.plugins.emailext.ExtendedEmailPublisher plugin="email-ext@2.39.3">
<recipientList>$DEFAULT_RECIPIENTS</recipientList>
<configuredTriggers>
<hudson.plugins.emailext.plugins.trigger.ScriptTrigger>
<email>
<recipientList>I_EXT_AC_TA_TEAM_CD@internal.nsn.com</recipientList>
<subject>[junit]$PROJECT_DEFAULT_SUBJECT</subject>
<body>$PROJECT_DEFAULT_CONTENT</body>
<recipientProviders>
<hudson.plugins.emailext.plugins.recipients.ListRecipientProvider/>
</recipientProviders>
<attachmentsPattern/>
<attachBuildLog>false</attachBuildLog>
<compressBuildLog>false</compressBuildLog>
<replyTo>no-reply@eslinv70</replyTo>
<contentType>project</contentType>
</email>
<triggerScript>
result=true build.getActions().each{ it -> if (it instanceof hudson.tasks.junit.TestResultAction) { result=it.getResult().isPassed() } } return !result
</triggerScript>
</hudson.plugins.emailext.plugins.trigger.ScriptTrigger>
</configuredTriggers>
<contentType>text/html</contentType>
<defaultSubject>$DEFAULT_SUBJECT</defaultSubject>
<defaultContent>${SCRIPT,template="junit_result.groovy"}</defaultContent>
<attachmentsPattern/>
<presendScript/>
<attachBuildLog>false</attachBuildLog>
<compressBuildLog>false</compressBuildLog>
<replyTo/>
<saveOutput>false</saveOutput>
<disabled>false</disabled>
</hudson.plugins.emailext.ExtendedEmailPublisher>
</publishers>
<buildWrappers>
<hudson.plugins.timestamper.TimestamperBuildWrapper plugin="timestamper@1.6"/>
</buildWrappers>
</project>'''

    ConfigureJenkins.get_config_jenkins("scm/locations/hudson.scm.SubversionSCM_-ModuleLocation/remote",cotnent.replace('\n',''))