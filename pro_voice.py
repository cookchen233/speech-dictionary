# coding=utf-8
import sys,os,threading
import pyaudio, wave
import xunfei_api
import requests
import urllib,urllib2
import baidu_api

from pydub import AudioSegment
import gevent
reload(sys)
sys.setdefaultencoding('utf-8')

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 8000
RECORD_SECONDS = 5

def mp3_url_to_wav(mp3_url, file='url.mp3'):
    # url = 'http://dict.youdao.com/dictvoice?audio=' + word
    # r = requests.get('http://dict.youdao.com/dictvoice?audio='+word)
    # with open('sound.mp3', 'wb') as f:
    #      f.write(r.content())

    urllib.urlretrieve(mp3_url, file)
    file = mp3_to_wav(file)
    return file

def mp3_to_wav(file):
    file_name = os.path.splitext(file)[0]
    sound = AudioSegment.from_mp3(file)
    file = file_name + '.wav'
    sound.export(file, format='wav')
    return file

def play(file):
    wf = wave.open(file, 'rb')
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

def record(file):
    print('recording....')
    global RECORDING, RECORD_RETURN
    RECORDING = True
    RECORD_RETURN = False
    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )
    frames = []
    while RECORDING:
        data = stream.read(CHUNK)
        frames.append(data)

    print("done")

    stream.stop_stream()
    stream.close()
    p.terminate()
    if file:
        wf = wave.open(file, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        RECORD_RETURN = file
    RECORD_RETURN = b''.join(frames)

def start_record(file=''):
    t = threading.Thread(target=record, args=(file, ))
    t.setDaemon(True)
    t.start()

def stop_record():
    global RECORDING
    RECORDING = False

def get_record():
    while RECORD_RETURN is False:
        pass
    return RECORD_RETURN