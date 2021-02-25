import requests
import json
import os

class KuWo(object):

    def __init__(self):

        self.headers = {
            "Cookie": "Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1613969685; _ga=GA1.2.373368830.1613969685; _gid=GA1.2.1071113528.1613969685; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1613970806; kw_token=21O69LPAXV8",
            "csrf": "21O69LPAXV8",
            "Host": "www.kuwo.cn",
            "Referer": "http://www.kuwo.cn",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
        }

    def get_url(self,pn=1,rn=1):
        keyword = input("请输入需要下载的歌曲：")
        return "http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key=%s&pn=%s&rn=%s" %(keyword,pn,rn)

    def parse_url(self,url):
        request = requests.get(url,headers=self.headers).text
        return request

    def get_song_url(self,request):
        result = json.loads(request)["data"]["list"][0]
        song_name = result["name"]
        rid = result["rid"]

        purl = "http://www.kuwo.cn/url?rid=%s&type=convert_url3&br=128kmp3" %(rid,)
        song_url = json.loads(self.parse_url(purl))["url"]
        return song_name,song_url

    def download(self,song_name,song_url):
        if not os.path.exists('music'):
            os.mkdir('music')
        with open('music/%s.mp3' %(song_name,),'wb') as f:
            music_mp3 = requests.get(song_url,timeout = 5).content
            f.write(music_mp3)
        print("success")

    def run(self):
        #1 准备url地址
        url = self.get_url()
        #2 发送请求，获取响应
        res = self.parse_url(url)
        #3 获取单曲url地址
        #4 发送请求，获取响应，解析出歌曲文件地址
        song_name,song_url = self.get_song_url(res)
        #5 保存为MP3文件
        self.download(song_name,song_url)
        
if __name__ == '__main__':
    kw = KuWo()
    kw.run()