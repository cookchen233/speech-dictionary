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
RATE = 44100
RECORD_SECONDS = 5
RECORDING = False

FILE_NAME = 'test.wav'

def play():
    # sound = AudioSegment.from_mp3('recorder.mp3')
    # sound.export('./recorder.wav', format='wav')
    sound = AudioSegment.from_wav('recorder.wav');
    sound.export('./recorder.mp3', format='mp3')
    wf = wave.open('recorder.wav', 'rb')
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

    wf = wave.open(fileName, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    t = threading.Thread(target=play)
    t.setDaemon(True)
    t.start()

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
g = record_generator('recorder.wav')
btn = Button ( root, textvariable=btn_text, command = g.next, width=100, height=6, highlightbackground='#3E4149')
btn.pack()
text_text = StringVar()
text_text.set('上对方上对方上对方的身份上对方的身份上对方上对方上对方的身份上对方的身份上对方上对方上对方的身份上对方的身份')
text = Message(root, textvariable=text_text, width=250)
text.pack()
root.geometry('300x400+800+200')

root.mainloop()  # 进入消息循环