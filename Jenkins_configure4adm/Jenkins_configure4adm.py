from modules.jenkins import Jenkins
from modules import errors
from modules.errors import ShellException
from modules.admjenkins import AdmJenkins
from modules.component import TrunkComponent

if __name__ == "__main__":
    items = "adaptations_trunk_see-Cloud16.2_ris"
    # jenkins jobs
    admjenkins = AdmJenkins(url = None, user = None, password = None)
    for item in items.split('/r/n'):
        item = item.strip()
        if not admjenkins.job_exists(item):
            print("[%s] jenkins dosen't exist" % item)
        svnpath = admjenkins.get_svnurl(item)
        if not svnpath:
            print("LOG failed")
            svnpath = "https://svne1.access.nokiasiemensnetworks.com/isource/svnroot/adaptations/trunk/NOKGOMS/NOKGOMS-FMO3.2/"
            #continue
        trunk = TrunkComponent(svnpath)
        commonpart = trunk.get_common_part()
        adapid, adaprelease = trunk.parse_svn_path()
        jobname = admjenkins.get_job_releaseid(adaprelease)
        if not jobname:
            print("LOG failed")
        manjobname = admjenkins.get_man_job(jobname)
        if not manjobname:
            print("LOG failed")
        if admjenkins.config_job(jobname,commonpart):
            print("LOG success")
        else:
            print("LOG failed")
        if admjenkins.create_job(jobname,commonpart):
            print("LOG success")
        else:
            print("LOG failed")