# coding=utf-8
import sys,io,json,threading
from Tkinter import *
import requests
import baidu_api,xunfei_api
import pro_voice
reload(sys)
sys.setdefaultencoding('utf-8')

def get_word(record_return):
    word = ''
    # try:
    #     result = xunfei_api.speech_stream_to_text(record_return)
    #     print '讯飞: ' + result[0]
    #     word = result[0]
    # except Exception as e:
    #     print '讯飞接口异常：'+str(e)
    try:
        result = baidu_api.speech_stream_to_text(record_return)
        print '百度: ' + result[0]
        word = result[0]
    except Exception as e:
        print '百度接口异常：'+str(e)
    return word.replace('，', '').replace('。', '')

def voice(word):
    mp3 = baidu_api.text_to_speech(word)
    wav = pro_voice.mp3_to_wav(mp3)
    pro_voice.play(wav)

def youdao_voice(word):
    wav = pro_voice.mp3_url_to_wav('http://dict.youdao.com/dictvoice?audio=' + word)
    pro_voice.play(wav)

def text_paraphrase(word):
    r = requests.get('http://www.iciba.com/index.php?callback=&a=getWordMean&c=search&list=&word=' + word)
    try:
        result = json.loads(r.text)
        symbols = result['baesInfo']['symbols'][0]
        message_text.set('\n'.join([
            symbols['ph_en'],
            symbols['ph_am'],
            symbols['parts'][0]['part'],
            '\n',
            '\n'.join(symbols['parts'][0]['means'])
        ]))
    except:
        message_text.set('查词异常')

def record_generator():
    while 1:
        btn_text.set('结束')
        pro_voice.start_record()
        yield
        pro_voice.stop_record()
        word = get_word(pro_voice.get_record())
        # youdao_voice('hello')
        if word:
            voice(word)
            youdao_voice(word)
        text_paraphrase(word)
        btn_text.set('开始说话')
        yield

root = Tk()

btn_text = StringVar()
btn_text.set('开始说话')
g = record_generator()
Button(root, textvariable=btn_text, command = g.next, width=100, height=6, highlightbackground='#3E4149').pack()

message_text = StringVar()
message_text.set('上对方上对方上对方的身份上对方的身份上对方上对方上对方的身份上对方的身份上对方上对方上对方的身份上对方的身份')
Message(root, textvariable=message_text, width=250).pack()

root.geometry('300x400+800+200')

root.mainloop()  # 进入消息循环