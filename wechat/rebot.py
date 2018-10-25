from werobot import WeRoBot
import re
from wechat.youtube import Youtubedl
import wechat.config as cfg
import sh
from wechat.utils import myTry, killProcess
from wechat.baidu import Baidu

myrobot = WeRoBot(token=cfg.token)
myrobot.config["APP_ID"] = cfg.appid
myrobot.config['ENCODING_AES_KEY'] = cfg.aeskey

#basic functions
@myTry
@myrobot.filter(re.compile("^start.*?"))
def start(message,session):
    message=message.content[6:]
    try:
        for i in session["content"]:
            session["content"][i]=False
        session["content"][message]=True
    except:
        session["content"]={}
        session["content"][message]=True
    session[message]=True
    return message+"启动"

@myTry
@myrobot.filter(re.compile("^stop.*?"))
def stop(message,session):
    message=message.content[5:]
    session[message]=False
    return message+"结束"

#youtube functions
@myTry
@myrobot.filter(re.compile("^yt1.*?"))
def yturl(url_raw,session):
    if(session['youtube']==True):
        url_raw=url_raw.content
        url=url_raw[url_raw.find(' ')+1:]
        youtubedl=Youtubedl(url)
        session['downloader']=youtubedl.toDict()
        return youtubedl.getinformation()
    else:
        return "请先启动youtube"

@myTry
@myrobot.filter(re.compile("^yt2.*?"))
def ytdld(message,session):
    if(session['youtube']==True):
        message=message.content
        v=message.find('v')
        a=message.find('a')
        n=message.find('n')
            
        vspace=message.find(' ',v)
        aspace=message.find(' ',a)

        video=message[v+1:vspace]
        audio=message[a+1:aspace]
        name=message[n+1:]

        downloader=Youtubedl('')
        downloader.fromDict(session['downloader'])
        session['downloader']['name']=name
        downloader.download(video,audio,name)
        return "下载中，请稍候"
    else:
        return "请先启动youtube"

@myTry
@myrobot.filter(re.compile("yt3"))
def ytded(message,session):
    if(session['youtube']==True):
        downloader=Youtubedl('')
        downloader.fromDict(session['downloader'])
        status=downloader.downloaded()
        if(not status):
            return "别急，还在下载"
        else:
            linkName=__file__[:__file__.find(__file__.split('/')[-1])]
            linkName+='static/youtubedl/'
            fileName=sh.head(sh.ls('-t',linkName),'-1')
            fileName=''.join(i for i in fileName)
            fileName=fileName[:fileName.find(' ')]
            killProcess(downloader.pid)

            bd=Baidu()
            bd.upload(linkName+fileName,fileName)

            return "下载完成，链接为： "+cfg.domain_youtubedl+fileName
    else:
        return "请先启动youtube"

@myTry
@myrobot.filter(re.compile("ytlist"))
def ytlist(message,session):
    if(session['youtube']==True):
        linkName=__file__[:__file__.find("rebot.py")]
        linkName+='static/youtubedl/'
        listdetail=sh.ls('-l',linkName)
        listdetail=''.join(i for i in listdetail)
        return listdetail
    else:
        return "请先启动youtube"

@myTry
@myrobot.filter(re.compile("^ytrmsingle.*?"))
def ytrmsingle(message,session):
    if(session['youtube']==True):
        linkName=__file__[:__file__.find("rebot.py")]
        linkName+='static/youtubedl/'
        message=message.content
        fileName=message[message.find(' ')+1:]
        linkName=linkName+fileName
        removeTask=sh.rm('-rf',linkName,_bg=True)
        removeTask.wait()
        return "删除"+linkName+"成功"
    else:
        return "请先启动youtube"

@myTry
@myrobot.filter(re.compile("ythelp"))
def ythelp(message,session):
    if(session['youtube']==True):
        content=r'''youtube help:
        ythelp:给出帮助信息
        yt1 <url>: 给出url对应的下载信息
        yt2 v<video> a<audio> n<name>: 下载对应视频
        yt3: 下载是否完毕，如果是，给出链接并自动上传百度网盘
        ytlist: 列出下载目录下所有文件
        ytrmsingle <name>: 删除下载目录下某文件
        '''
        return content
    else:
        return "请先启动youtube"

@myTry
@myrobot.filter(re.compile("^ytbd.*?"))
def ytbd(message,session):
    if(session['youtube']==True):
        bd=Baidu()
        message=message.content
        message=message[5:]
        if(bd.checkUpload(message)):
            return "上传"+message+"已完成"
        else:
            return "还未完成"
    else:
        return "请先启动youtube"

#baidu cloud
@myTry
@myrobot.filter(re.compile("^bd1.*?"))
def bd1(message,session):
    if(session['baidu']==True):
        message=message.content
        message=message[4:]
        url=message[:message.find(' ')]
        name=message[message.find(' ')+1:]

        bd=Baidu()
        bd.remoteDownload(url,name)
        session['baidupid']=bd.pid
        return "开始下载"
    else:
        return "请先启动baidu"

@myTry
@myrobot.filter(re.compile("^bd2.*?"))
def bd2(message,session):
    if(session['baidu']==True):
        message=message.content
        name=message[4:]


        bd=Baidu()
        bd.pid=session['baidupid']
        status=bd.checkremoteDownload(name)
        if(status==False):
            return "还没下载完毕"
        else:
            return "下载链接为"+status
    else:
        return "请先启动baidu"