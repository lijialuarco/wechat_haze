# coding=utf-8

from datetime import datetime
import datetime as dt
import itchat
from itchat.content import *
import image_analyser


def get_image_names(date_range):
    if date_range == 1:
        return image_analyser.get_images([datetime.today().strftime('%Y-%m-%d')])
    if date_range == 7:
        date_list = []
        for i in range(-1, 6):
            date_list.append((datetime.now() + dt.timedelta(days=i)).strftime('%Y-%m-%d'))
        return image_analyser.get_images(date_list)


def text_analyser(text):
    return_text = '关键词未匹配'
    if text.find('雾霾') == -1:
        return return_text

    if text.find('今日') != -1 or text.find('今天') != -1:
        return get_image_names(1)

    if text.find('七天') != -1 or text.find('七日') != -1:
        return get_image_names(7)

    if text.find('7天') != -1 or text.find('7日') != -1:
        return get_image_names(7)

    return return_text


# # 包括文本、位置、名片、通知、分享
# @itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
# def text_reply(msg):
#     # 微信里，每个用户和群聊，都使用很长的ID来区分
#     # msg['FromUserName']就是发送者的ID
#     # 将消息的类型和文本内容返回给发送者
#     itchat.send('%s: %s' % (msg['Type'], msg['Text']), msg['FromUserName'])
#
#
# # 处理多媒体类消息
# # 包括图片、录音、文件、视频
# @itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
# def download_files(msg):
#     # msg['Text']是一个文件下载函数
#     # 传入文件名，将文件下载下来
#     msg['Text'](msg['FileName'])
#     # 把下载好的文件再发回给发送者
#     return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])
#
#
# # 处理好友添加请求
# @itchat.msg_register(FRIENDS)
# def add_friend(msg):
#     # 该操作会自动将新好友的消息录入，不需要重载通讯录
#     itchat.add_friend(**msg['Text'])
#     # 加完好友后，给好友打个招呼
#     itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])


# 处理群聊消息
@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if msg['isAt']:
        ret = text_analyser(msg['Text'])
        if ret == '关键词未匹配':
            itchat.send(u'@%s\u2005我不是很懂: %s' % (msg['ActualNickName'], msg['Content']), msg['FromUserName'])
        else:
            print(itchat.send_image('s.png', msg['FromUserName']))


# 在auto_login()里面提供一个True，即hotReload=True
# 即可保留登陆状态
# 即使程序关闭，一定时间内重新开启也可以不用重新扫码
itchat.auto_login(True)
itchat.run()
