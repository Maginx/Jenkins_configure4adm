
from mimify import File
import os
import shutil
from modules.logger import TraceLog

class FileHandler(File):
    '''File operation class
    '''
    @classmethod
    def copyfile(cls,sourceFile, destFile):
        '''Move file or folder form source to dest
        '''
        try:
            if os.path.exists(destFile):
                os.remove(destFile)
            shutil.copyfile(sourceFile,destFile)
        except  IOError:
            TraceLog.warning("copy file failed from [%s] to [%s]" % (sourceFile, destFile))
            return False
        return True
