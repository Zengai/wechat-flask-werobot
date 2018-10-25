# Flask与Werobot实现个性化微信订阅号
这是我的wechat订阅号个人应用，正在不断完善中。

目前实现的功能有：
1. 提供了一个结合flask和werobot的总体框架。
2. 实现了远程利用youtubedl下载文件的功能。
3. 利用bypy实现了与百度网盘的接口,可以将下载的文件存入百度网盘，或使用遥控百度进行外链下载。

建议使用anaconda配置环境。对于anaconda:
```bash
conda install ffmpeg
pip install -r packages.txt
```
另外还要在wechat文件夹中加入config.py文件，格式为:
```config
domain_youtubedl="http://<你的域名>/static/youtubedl/"
token="<微信token接口>"
appid="<订阅号appid>"
aeskey='<订阅号aeskey>'
```
使用时可直接在本程序包主目录下运行：（建议在screen中运行）
```bash
./run.sh
```
此外为支持百度云盘功能，还需要先在命令行运行bypy info登录百度云。下载视频在/app/upload/目录下。