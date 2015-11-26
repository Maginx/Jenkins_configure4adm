import sys
sys.path.append('.')
from modules import errors
from modules.admjenkins import AdmJenkins
from modules.component import TrunkComponent
from modules.logger import TraceLog

if __name__ == "__main__":
    items = "adap_ci_test_adm-jenkins_ris"
    # jenkins jobs
    adm_jenkins = AdmJenkins(url = None, user = None, password = None)
    for item in items.split('/n'):
        item = item.strip()
        TraceLog.info(u"---------- <b>%s</b> ----------" % item)
        TraceLog.info("Check jenkins job exist or not [%s]" % item)
        # verify jenkins job exist or not
        if not adm_jenkins.job_exists(item):
            TraceLog.error("jenkins job doesn't exsit [%s]" % item)
            TraceLog.failed_job(item)
            continue
        # get corresponding svn path
        svnpath = adm_jenkins.get_svnurl(item)
        if not svnpath:
             TraceLog.error("jenkins job svn path not exist <b>[%s]</b>" % svnpath)
             TraceLog.failed_job(item)
             continue
        trunk = TrunkComponent(svnpath)
        commonpart = trunk.get_common_part()
        adapid, adaprelease = trunk.parse_svn_path()
        if not adm_jenkins.job_exists(item):
            TraceLog.failed_job(item)
            continue
        TraceLog.info("config jenkins job <b>[%s]</b>" % item)
        if adm_jenkins.config_job(item, commonpart):
            TraceLog.success_job(item)
        else:
            TraceLog.failed_job(item)
        manjobname = adm_jenkins.get_man_job(item)
        if adm_jenkins.job_exists(manjobname):
            TraceLog.info("man job exist now.")
            continue
        TraceLog.info("create jenkins job <b>[%s]</b>" % manjobname)
        if adm_jenkins.create_job(manjobname,commonpart):
            TraceLog.success_job(manjobname)
        else:
            TraceLog.failed_job(manjobname)
        TraceLog.info("created jenkins job <b>[%s]</b>" % manjobname)
        