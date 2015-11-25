from mimify import File
import os
import shutil
from datetime import datetime
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
    
    @classmethod
    def create_temp_file(cls, content, name = None):
        '''Create temp file 
        @param content : file content,string
        @param name : file name, if none, the temp file name format will be yy-mm-dd HH:MM:SS,string
        @return filename
        '''
        name = str(datetime.now()) if not name else name + "-" + str(datetime.now()) 
        with open(name, 'wt') as write:
            write.write(content)
        return name

    @classmethod
    def delete_temp_file(cls, name):
        '''Delete temp file by file name
        @param name : file name,string
        '''
        if os.path.exists(name):
            os.remove(name)