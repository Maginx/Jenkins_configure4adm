import logging

class TraceLog(object):
    '''Trace program process infomation and  stdout to console out
    '''

    __logger = logging.getLogger("info")
    __logger.setLevel(logging.DEBUG)
    __streamhandler = logging.StreamHandler()
    __formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    __streamhandler.setFormatter(__formatter)
    __logger.addHandler(__streamhandler)

    __job_format = "%s - job name : %s"
    __file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(message)s")

    __success_index = 1
    __file_success_logger = logging.getLogger("success")
    __file_success_logger.setLevel(logging.DEBUG)
    __successhandler = logging.FileHandler("success_jenkins")
    __successhandler.setFormatter(__file_formatter)
    __file_success_logger.addHandler(__successhandler)

    __failed_index = 1
    __file_failed_logger = logging.getLogger("failed")
    __file_failed_logger.setLevel(logging.DEBUG)
    __failedhandler = logging.FileHandler("failed_jenkins")
    __failedhandler.setFormatter(__file_formatter)
    __file_failed_logger.addHandler(__failedhandler)

    @classmethod   
    def info(cls,message):
       TraceLog.__logger.info(message)
    
    @classmethod
    def excepiton(cls,e):
        TraceLog.__logger.exception(e)
    
    @classmethod
    def error(cls, message):
        TraceLog.__logger.error(message)
        
    @classmethod
    def warning(cls, message):
        TraceLog.__logger.warn(message)
    
    @classmethod
    def success_job(cls, jobName):
        TraceLog.__file_success_logger.info(TraceLog.__job_format % (TraceLog.__success_index, jobName))
        TraceLog.__success_index = TraceLog.__success_index + 1
    
    @classmethod
    def failed_job(cls, jobName):
        TraceLog.__file_failed_logger.info(TraceLog.__job_format % (TraceLog.__failed_index, jobName))
        TraceLog.__failed_index = TraceLog.__failed_index + 1

if __name__ == "__main__":
    TraceLog.info("TEST")
    TraceLog.success_job("adap_ci_success_1_ri1s")
    TraceLog.success_job("adap_ci_success_2_ri1s")   
    TraceLog.failed_job("adap_ci_failed_1_ris")
    TraceLog.failed_job("adap_ci_failed_2_ris")
