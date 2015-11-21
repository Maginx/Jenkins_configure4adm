
from mimify import File
import os
import shutil

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
            print("copy job configure file error, %s %s" % (sourceFile, destFile))
            return False
        return True
