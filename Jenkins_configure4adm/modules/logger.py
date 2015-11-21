import logging

class TraceLog(object):
    '''Trace program process infomation and  stdout to console out
    '''
    logger =  logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    streamhandler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    streamhandler.setFormatter(formatter)
    logger.addHandler(streamhandler)   

    @classmethod   
    def info(cls,message):
       TraceLog.logger.info(message)
    
    @classmethod
    def excepiton(cls,e):
        TraceLog.logger.exception(e)
    
    @classmethod
    def error(cls, message):
        TraceLog.logger.error(message)

    @classmethod
    def warn(cls, message):
        TraceLog.logger.warn(message)

if __name__ == "__main__":
    TraceLog.info("TEST")
    try:
       raise ValueError("Test value error")
    except  ValueError, e:
        TraceLog.excepiton(e)
       