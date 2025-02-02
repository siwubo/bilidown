import re
import requests
import json
from contextlib import closing

cookie = '''请填写你的哔哩哔哩cookies'''

header = {
'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
'Cookie': cookie,
'Origin': 'https://www.bilibili.com',
'accept': 'application/json',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en-US,en;q=0.8',
'content-type': 'application/json',
'Referer': 'https://www.bilibili.com'
}
 
print("""
/*********************/
支持分集下载 支持的链接格式如下
https://b23.tv/*
https://www.bilibili.com/video/BV*
https://www.bilibili.com/video/av*
Github：https://github.com/5ime/bilidown
/*********************/
""")

url = input("输入哔哩哔哩视频链接:")
if 'https://b23.tv' in url: 
    loc = requests.get(url,allow_redirects=False)
    url = loc.headers['location'] 
if 'video/av' in url:
    av = json.loads(requests.get('https://api.bilibili.com/x/web-interface/archive/stat?aid='+url,allow_redirects=False,headers=header).text)
    url = av['data']['bvid']
video_id = re.findall("[\w.]*[\w:\-\+\%]",url)[3]
vid = json.loads(requests.get('https://api.bilibili.com/x/web-interface/view?bvid='+video_id,allow_redirects=False,headers=header).text)
video = vid['data']['pages'][0]['cid']
page = 0
if vid['data']['videos'] > 1:
    page = int(input("这是一个多P视频,共%d集,请输入要下载第几集(例如：1)并回车："%vid['data']['videos']))
    page -= 1
    video = vid['data']['pages'][page]['cid']
video_info = json.loads(requests.get('https://api.bilibili.com/x/player/playurl?bvid='+video_id+'&cid='+str(video)+'&qn=80&otype=json',allow_redirects=False,headers=header).text)
video_name = vid['data']['title']
video_url = video_info['data']['durl'][0]['url']

print("\n******获取成功******\n视频标题：%s\n下载链接：%s"%(video_name,video_url))
print("""
正在自动下载视频中，切勿关闭窗口
如下载失败请自行复制下载链接下载(需设置Referer)
""")

def Download(video_url,video_name,header):
    with closing(requests.get(video_url,headers=header,stream=True)) as response:
        chunk_size = 1024  # 单次请求最大值
        content_size = int(response.headers['content-length'])  # 内容体总大小
        data_count = 0
        with open(video_name+'.flv','wb') as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                data_count = data_count + len(data)
                now_jd = (data_count / content_size) * 100
                print("\r视频下载进度：%d%%(%d/%d)" % (now_jd, data_count, content_size), end=" ")
            input('\n\n下载成功！下载的视频位于本程序同级目录中,按回车退出程序...')
Download(video_url,video_name,header)
