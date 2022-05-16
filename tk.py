# coding=utf-8
import sys, threading,io,json
import pyaudio, wave
from Tkinter import *
import requests
import urllib,urllib2
import baidu_api
import xunfei_api

from pydub import AudioSegment
reload(sys)
sys.setdefaultencoding('utf-8')

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 8000
RECORD_SECONDS = 5
RECORDING = False

FILE_NAME = 'test.wav'

def play(word):
    url = 'http://media.shanbay.com/audio/us/hello.mp3'
    url = 'http://media.shanbay.com/audio/uk/hello.mp3'
    url = 'http://dict.youdao.com/dictvoice?audio=' + word
    # r = requests.get('http://dict.youdao.com/dictvoice?audio='+word)
    # with open('sound.mp3', 'wb') as f:
    #      f.write(r.content())
    urllib.urlretrieve(url, 'sound.mp3')

    sound = AudioSegment.from_mp3('sound.mp3')
    sound.export('./sound.wav', format='wav')

    wf = wave.open('sound.wav', 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(),
                    rate=wf.getframerate(), output=True)
    data = wf.readframes(CHUNK)
    while data != '':
        stream.write(data)
        data = wf.readframes(CHUNK)
    stream.stop_stream()
    stream.close()
    p.terminate()

def record_thread(fileName, stream, p):
    print('recording....')

    frames = []
    while RECORDING:
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # wf = wave.open(fileName, 'wb')
    # wf.setnchannels(CHANNELS)
    # wf.setsampwidth(p.get_sample_size(FORMAT))
    # wf.setframerate(RATE)
    # wf.writeframes(b''.join(frames))
    # wf.close()

    # result = baidu_api.speech_to_text2(FILE_NAME)
    result = baidu_api.speech_stream_to_text(b''.join(frames))
    # result2 = xunfei_api.speech_stream_to_text(b''.join(frames))
    print '百度: '+result[0]
    # print '讯飞: '+result2[0]
    t = threading.Thread(target=play, args=(result[0],))
    t.setDaemon(True)
    t.start()
    r = requests.get('http://www.iciba.com/index.php?callback=&a=getWordMean&c=search&list=&word='+result[0])
    result = json.loads(r.text)
    symbols = result['baesInfo']['symbols'][0]
    text_text.set('\n'.join([
        symbols['ph_en'],
        symbols['ph_am'],
        symbols['parts'][0]['part'],
        '\n',
        '\n'.join(symbols['parts'][0]['means'])
    ]))

def record_generator(fileName):
    global RECORDING
    while 1:
        btn_text.set('结束')
        RECORDING = True
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        t = threading.Thread(target=record_thread, args=(fileName, stream, p))
        t.setDaemon(True)
        t.start()
        yield
        RECORDING = False
        btn_text.set('开始说话')
        yield

root = Tk()  # 创建窗口对象的背景色
btn_text = StringVar()
btn_text.set('开始说话')
g = record_generator('test.wav')
btn = Button ( root, textvariable=btn_text, command = g.next, width=100, height=6, highlightbackground='#3E4149')
btn.pack()
text_text = StringVar()
text_text.set('上对方上对方上对方的身份上对方的身份上对方上对方上对方的身份上对方的身份上对方上对方上对方的身份上对方的身份')
text = Message(root, textvariable=text_text, width=250)
text.pack()
root.geometry('300x400+800+200')

root.mainloop()  # 进入消息循环