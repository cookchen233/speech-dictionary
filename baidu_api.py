# -*- coding: UTF-8 -*-

from pydub import AudioSegment
from aip import AipSpeech
import json
""" 你的 APPID AK SK """
APP_ID = '11671525'
API_KEY = 'xIQTTyoPaN2oXmKNWrRQ2ymD'
SECRET_KEY = 'vBZPfzK5mWbwiGyqR63DPB4TzaLNTjxr'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

'''
dev_pid	语言	模型	是否有标点	备注
1536	普通话(支持简单的英文识别)	搜索模型	无标点	支持自定义词库
1537	普通话(纯中文识别)	输入法模型	有标点	不支持自定义词库
1737	英语		有标点	不支持自定义词库
1637	粤语		有标点	不支持自定义词库
1837	四川话		有标点	不支持自定义词库
1936	普通话远场	远场模型	有标点	不支持
'''
def speech_file_to_text(filename):
    with open(filename, 'rb') as fp:
        file_content = fp.read()
        return speech_to_text(file_content)

def speech_stream_to_text(file_content):
    return speech_to_text(file_content)

def speech_to_text(file_content):
    result = client.asr(file_content, 'wav', 16000, {
        'dev_pid': 1737,
    })
    if result['err_no'] == 0:
        return result['result']
    if result['err_no'] == 3301:
        return ['']
    raise Exception(result['err_msg'])

'''
参数	类型	描述	是否必须
tex	String	合成的文本，使用UTF-8编码，
请注意文本长度必须小于1024字节	是
cuid	String	用户唯一标识，用来区分用户，
填写机器 MAC 地址或 IMEI 码，长度为60以内	否
spd	String	语速，取值0-9，默认为5中语速	否
pit	String	音调，取值0-9，默认为5中语调	否
vol	String	音量，取值0-15，默认为5中音量	否
per	String	发音人选择, 0为女声，1为男声，
3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女	否
'''
def text_to_speech(text, file='speech.mp3'):
    result = client.synthesis(text, 'zh', 1, {
        'vol': 5,
    })
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open(file, 'wb') as f:
            f.write(result)
            return file
    raise Exception(result['err_msg'])

