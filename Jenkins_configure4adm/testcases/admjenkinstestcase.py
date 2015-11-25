import unittest
import mock
import sys
sys.path.append(sys.path[0].split('testcases')[-2])
import modules.admjenkins

class AdmJenkinsTestCase(unittest.TestCase):
    
    def setUp(self):  
        self.adm = modules.admjenkins.AdmJenkins(url=None,user=None,password=None)   
        self.jobname = "adap"
        self.manjobname = "adap_test"
        self.commonpart = "commonpart_test"
    def tearDown(self):  
        self.adm = None 

    @mock.patch(target = "modules.admjenkins.AdmJenkins.reconfig_job")
    @mock.patch(target = "modules.admjenkins.AdmJenkins.get_man_job")
    @mock.patch(target = 'modules.admjenkins.AdmJenkins.get_job_xml_filepath')
    def test_config_job(self, mock_get_job_xml, mock_get_man_job, mock_reconfig_job):
        mock_get_job_xml.return_value = "D:\userdata\j69wang\Desktop\config.xml"
        mock_get_man_job.return_value = self.manjobname
        mock_reconfig_job.return_value = True
        result = self.adm.config_job(self.jobname, self.commonpart)        
        self.assertTrue(result)
    
    @mock.patch(target = "modules.jenkins.Jenkins.create_job")
    @mock.patch(target = "modules.admjenkins.AdmJenkins.job_exists")
    def test_create_job(self, mock_job_exists, mock_create_job):
        mock_create_job.return_value = True
        mock_job_exists.return_value = False

        result = self.adm.create_job(self.manjobname,self.commonpart)

        self.assertTrue(result)



if __name__ == "__main__":     
    unittest.main()