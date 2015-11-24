import sys
sys.path.append('.')
from modules.jenkins import Jenkins
from modules import errors
from modules.errors import ShellException
from modules.admjenkins import AdmJenkins
from modules.component import TrunkComponent
from modules.logger import TraceLog

if __name__ == "__main__":
    items = "adap_ci_test_adm-jenkins_ris"
    # jenkins jobs
    admjenkins = AdmJenkins(url = None, user = None, password = None)
    for item in items.split('/r/n'):
        item = item.strip()
        TraceLog.info(u"\nConfiguring jenkins job ---------- %s ----------" % item)
        TraceLog.info("Check jenkins job exist or not [%s]" % item)
        if not admjenkins.job_exists(item):
            TraceLog.error("jenkins job doesn't exsit [%s]" % item)
            TraceLog.failed_job(item)
            continue
        svnpath = admjenkins.get_svnurl(item)
        if not svnpath:
             TraceLog.error("jenkins job svn path not exist [%s]" % svnpath)
             TraceLog.failed_job(item)
             continue
        trunk = TrunkComponent(svnpath)
        commonpart = trunk.get_common_part()
        adapid, adaprelease = trunk.parse_svn_path()
        if not admjenkins.job_exists(item):
            TraceLog.failed_job(item)
            continue
        TraceLog.info("config jenkins job %s" % item)
        if admjenkins.config_job(item,commonpart):
            TraceLog.success_job(item)
        else:
            TraceLog.failed_job(item)
        manjobname = admjenkins.get_man_job(item)
        if admjenkins.job_exists(manjobname):
            TraceLog.info("man job exist now.")
            continue
        TraceLog.info("create jenkins job %s" % manjobname)
        if admjenkins.create_job(manjobname,commonpart):
            TraceLog.success_job(manjobname)
        else:
            TraceLog.failed_job(manjobname)
        