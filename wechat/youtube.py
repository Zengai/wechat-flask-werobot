import sh 
from wechat.utils import time_limit, check_pid

class Youtubedl(object):
    def __init__(self,url):
        self.url=url
        self.name=None
        self.pid=None
        self.youtubedl=sh.Command("youtube-dl")
        self.video=None
        self.audio=None
    def getinformation(self):
        que1=self.youtubedl("-F",self.url)
        text='\n'.join(i for i in que1)
        return text
    def download(self,video,audio,dir):
        path=__file__[:__file__.find(__file__.split('/')[-1])]
        self.name=dir
        dir=path+"static/youtubedl/"+dir
        self.que2=self.youtubedl("-f",video+"+"+audio,self.url,"-o",dir,_bg=True)
        self.pid=self.que2.pid 
        return True
    def downloaded(self):
            linkName=__file__[:__file__.find(__file__.split('/')[-1])]
            linkName+='static/youtubedl/'
            fileName=self.name+'.mkv'
            content=''.join(i for i in sh.ls(linkName))
            if(fileName in content):
                return True
            else:
                return False
    
    def toDict(self):
        return {'url':self.url,'name':self.name,'pid':self.pid}

    def fromDict(self,theDict):
        self.url=theDict['url']
        self.name=theDict['name']
        self.pid=theDict['pid']