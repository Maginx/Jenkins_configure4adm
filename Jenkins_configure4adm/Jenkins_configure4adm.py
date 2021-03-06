﻿import sys
sys.path.append('.')
from modules.jenkins import Jenkins
from modules import errors
from modules.errors import ShellException
from modules.admjenkins import AdmJenkins
from modules.component import TrunkComponent
from modules.logger import TraceLog

if __name__ == "__main__":
    items = "adap_ci_test_adm_jenkins_ris"
    # jenkins jobs
    admjenkins = AdmJenkins(url = None, user = None, password = None)
    for item in items.split('/r/n'):
        item = item.strip()
        print(u"\nConfiguring jenkins job ---------- %s ----------" % item)
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
        jobname = admjenkins.get_job_releaseid(adaprelease)
        if not jobname:
            TraceLog.failed_job(jobname)
            continue
        manjobname = admjenkins.get_man_job(jobname)
        if admjenkins.config_job(jobname,commonpart):
            TraceLog.success_job(jobname)
        else:
            TraceLog.failed_job(jobname)
        if admjenkins.create_job(jobname,commonpart):
            TraceLog.success_job(jobname)
        else:
            TraceLog.failed_job(jobname)
        