# !/usr/bin/python
# -*- coding: utf-8 -*-
import os
from moviepy.editor import *
import hashlib
import json
from Crypto.Cipher import AES
from binascii import b2a_hex
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import time
import pyautogui
import requests
from moviepy.editor import *
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()


class Item(BaseModel):
    url: str = None
    name: str = None

#这是将python作为了一个web服务端，来接受参数的，我用的post请求，主要接受转换视频的链接和音乐名字
@app.post('/wyy')
def calculate(request_data: Item):
    url = request_data.url
    name = request_data.name
    try:
        mp3(url, name)

        res = {"res": 0}
    except:
        res = {"res": 1}
    return res


# 模拟设备
headers = {
    'Cookie': '你的网易云cookie，后期会实现账号登录版本',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko)',
    'Content-Type': 'application/x-www-form-urlencoded'
}


# 传入url和name


# 下载mp3
def mp3(url, name):
    url = "这里是我的短视频解析地址，用于下载视频文件" + url
    r = requests.get(url)
    print("解析成功")
    rr = r.json()
    rrr = rr['url']
    print(rrr)
    mp4 = requests.get(rrr)
    content = mp4.content
    with open(r"C:\Users\Administrator\Desktop\wyy\111.mp4", "wb") as f:
        f.write(content)
    print("视频下载成功")

    name = name
    #这里开始转换为mp3格式并上传
    Upload(name)




# 加密接口
def eapi_encrypt(path, params):
    """eapi
    接口参数加密
    :param bytes path: 请求的路径
    :param params: 请求参数
    :return str: 加密结果
    """
    print('获取加密')
    params = json.dumps(params, separators=(',', ':')).encode()
    sign_src = b'nobody' + path + b'use' + params + b'md5forencrypt'
    m = hashlib.md5()
    m.update(sign_src)
    sign = m.hexdigest()
    aes_src = path + b'-36cd479b6b5-' + params + b'-36cd479b6b5-' + sign.encode()
    pad = 16 - len(aes_src) % 16
    aes_src = aes_src + bytearray([pad] * pad)
    crypt = AES.new(b'e82ckenh8dichen8', AES.MODE_ECB)
    ret = crypt.encrypt(aes_src)
    return b2a_hex(ret).upper()


# 获取md5
def getmd5(file):
    m = hashlib.md5()
    with open(file, 'rb') as f:
        for line in f:
            m.update(line)
    md5code = m.hexdigest()
    print(md5code)
    return md5code


# 上传
def up(filename, name):
    url = 'http://music.163.com/eapi/cloud/upload/check'
    # 需要的三个参数
    """
            上传前检查，获取songId
            :param str md5: 文件MD5
            :param int length: 文件大小(byte)
            :param int bit_rate: 音乐码率
            :param str ext: 扩展名
            :return dict:
            """
    md5 = getmd5(filename)
    length = os.path.getsize(filename)
    bit_rate = '320000'
    ext = 'wav'
    params = {
        'md5': md5,
        'length': str(length),
        'bitrate': str(bit_rate),
        'ext': ext,
        'version': '1',
        'verifyId': 1,
        'os': 'OSX',
        'header': '{"os":"osx","appver":"1.5.9","requestId":"85570439","clientSign":""}'}
    # print(params)
    path = b'/api/cloud/upload/check'
    params = 'params=' + eapi_encrypt(path, params).decode()
    # print(params)
    print('开始上传文件')
    # files = {'file': open(filename, 'rb')}
    # print(files)
    response = json.loads(requests.post(url, headers=headers, data=params, verify=False).text)
    # print(response)
    song_id = response['songId']
    song = name
    artist = '小众'
    bit_rate = 32000
    cloud_upload_info(md5, song_id, filename, song, artist, bit_rate, name)


def cloud_upload_info(file, song_id, filename, song, artist, bit_rate, name):
    """
        设置上传文件的信息
        :param md5: 文件MD5
        :param 'song_id': 歌曲ID
        :param filename: 文件名
        :param song: 歌曲名
        :param artist: 艺术家名
        :param bit_rate: 码率
        :return dict:
        """
    url = 'https://musicupload.netease.com/eapi/upload/cloud/info/v2'
    print('上传歌曲信息等')
    params = {
        'md5': file,
        'songid': song_id,
        'filename': filename,
        'song': song,
        'picUrl': 'https://image.baidu.com/search/detail?ct=503316480&z=&tn=baiduimagedetail&ipn=d&word=%E9%9F%B3%E4%B9%90%E7%9A%84%E5%8A%9B%E9%87%8F&step_word=&ie=utf-8&in=&cl=2&lm=-1&st=-1&hd=&latest=&copyright=&cs=2408022859,1225376201&os=941954127,1803206217&simid=3560859132,289641990&pn=7&rn=1&di=116820&ln=727&fr=&fmq=1607880598879_R&ic=&s=undefined&se=&sme=&tab=0&width=&height=&face=undefined&is=0,0&istype=2&ist=&jit=&bdtype=0&spn=0&pi=0&gsm=0&objurl=http%3A%2F%2Fmmbiz.qpic.cn%2Fmmbiz_png%2FzKBwDdu8U8FoAGmmiac6uRBF6zBsVxGt7dRNAyibibuH41icvAoSKH76TnlVoKe1Z3AiaFF1RQicYYnt4k8icWXNQlebQ%2F0%3Fwx_fmt%3Dpng&rpstart=0&rpnum=0&adpicid=0&force=undefined',
        'artist': artist,
        'bitrate': bit_rate,
    }
    path = b'/api/upload/cloud/info/v2'
    # print(params)
    params = 'params=' + eapi_encrypt(path, params).decode()
    # print(params)

    response = requests.post(url, headers=headers, data=params, verify=False).text
    # print(response)
    id = json.loads(response)['code']
    print(id)
    params = {
        'songid': str(song_id),
    }
    url = 'http://music.163.com/eapi/v1/cloud/get'
    path = b'/api/v1/cloud/get'
    params = 'params=' + eapi_encrypt(path, params).decode()
    # print(params)
    resp = requests.post(url, headers=headers, data=params, verify=False).text
    # print(resp)


def Upload(name):
    video = VideoFileClip(r"C:\Users\Administrator\Desktop\wyy\111.mp4")
    print('kaishizhuanhuan')
    audio = video.audio
    audio.write_audiofile(r"C:\Users\Administrator\Desktop\wyy\222.wav")
    print("音乐转换成功")
    user = pyautogui.locateOnScreen(r"C:\Users\Administrator\Desktop\wyy\up.png")
    goto = pyautogui.center(user)
    pyautogui.moveTo(goto)
    pyautogui.click()
    print("正在上传至网易云盘")
    time.sleep(1)
    pyautogui.moveRel(0, -70)
    pyautogui.click()
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    print("上传成功")
    a = 1
    #这里为什么要用到for循环，主要就是判断视频是否长传成功。
    for i in range(99999):
        if a == 1:
            try:
                print("第二次转换")
                video = VideoFileClip(r"C:\Users\Administrator\Desktop\wyy\111.mp4")
                print('kaishizhuanhuan')
                audio = video.audio
                audio.write_audiofile(r"C:\Users\Administrator\Desktop\wyy\222.wav")
                print("音乐转换成功")
                a = 0
            except:
                print("报错了，说明上传失败")
                a = 1
        else:
            break
#这个是用来更新音乐文件信息的
    up(r"C:\Users\Administrator\Desktop\wyy\222.wav", name)


if __name__ == '__main__':
    import uvicorn
#这里的555，是启动web端的端口号
    uvicorn.run(app=app,
                host="0.0.0.0",
                port=555,
                workers=1)
