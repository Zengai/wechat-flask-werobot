import sh
import wechat.config as cfg
import os
import time
from wechat.utils import killProcess
import wechat.config as cfg

class Baidu(object):
    def __init__(self):
        self.bp=sh.Command('bypy')
        self.pid=None
    def list(self,dir):
        ls=self.bp.bake("list")
        content=''.join(i for i in ls(dir))
        return content
    def upload(self,dir,name):
        self.bp("upload",dir,"/upload/"+name,_bg=True)
        return True
    def checkUpload(self,name):
        ck=self.bp("list","/upload/")
        content=''.join(i for i in ck)
        status=content.find(name)
        if(status==-1):
            return False
        else:
            return True
    def remoteDownload(self,url,name):
        linkName=__file__[:__file__.find(__file__.split('/')[-1])]
        linkName+='static/remote/'
        task=sh.wget("-c",url,"-O",linkName+name,_bg=True)
        self.pid=task.pid
        return True
    def checkremoteDownload(self,name):
        linkName=__file__[:__file__.find(__file__.split('/')[-1])]
        linkName+='static/remote/'
        filesize1=os.path.getsize(linkName+name)
        time.sleep(2)
        filesize2=os.path.getsize(linkName+name)
        if(filesize1==filesize2):
            killProcess(self.pid)
            self.bp("upload",linkName+name,"/offlineDownload/"+name,_bg=True)
            return cfg.domain_remote+name
        else:
            return False