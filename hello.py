# coding=utf-8
import sys, threading,io,json
import xunfei_api
import baidu_api
import pro_voice

result = xunfei_api.speech_file_to_text('test.wav')
print result
mp3 = baidu_api.text_to_speech('你好')
wav = pro_voice.mp3_to_wav(mp3)
pro_voice.play(wav)