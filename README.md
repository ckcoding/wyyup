# wyyup
网易云云盘上传（待完善，目前可用）

首先，这是一个曲线救国的版本，目前而言，已经是最优解决方案了。

需求：我在抖音，快手遇见一些好听的歌，想通过脚本实现把这些歌曲上传到网易云云盘。

需求分析：首先需要将短视频链接分析出来，并下载保存到本地，然后将歌曲转换为mp3格式，然后通过网易云接口上传到服务器，并且，将歌曲名字，作者，修改为自己填写的内容。

我是如何做的？

1:短视频链接分析（脚本实现，自研）
2:下载到本地（脚本实现，很简单）
3:将歌曲转换为mp3（脚本实现，引入第三方大佬的包，from moviepy.editor import *）
4:通过接口上传到网易云云盘（脚本可实现绝大部分，借鉴改编自这位大佬的方式：https://github.com/picone/CloudMusicUploader）

前面为什么说是一个曲线救国的方法呢，因为，在第4点的上传方式，借助了模拟点击，需要配合网易云客户端。（无法通过纯脚本实现，这是一点遗憾，但是勉强可用）

#这是上传代码，主要借助pyautogui，通过事前的截图分析定位，然后模拟鼠标点击，达到上传的目的。
import pyautogui
def up:()
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
up()

最后付一份上传用到的主要源码
