# -*- coding: UTF-8 -*-
import urllib2
import time
import urllib
import json
import hashlib
import base64

def speech_file_to_text(filename):
    f = open(filename, 'rb')
    file_content = f.read()
    return speech_to_text(file_content)

def speech_stream_to_text(file_content):
    return speech_to_text(file_content)

def speech_to_text(file_content):
    base64_audio = base64.b64encode(file_content)
    body = urllib.urlencode({'audio': base64_audio})

    url = 'http://api.xfyun.cn/v1/service/v1/iat'
    api_key = '2a9a8a1019752b4f7fd7b64f29c1b6e0'
    x_appid = '5b704f75'
    param = {"engine_type": "sms16k", "aue": "raw"}
    x_param = base64.b64encode(json.dumps(param).replace(' ', ''))
    x_time = int(int(round(time.time() * 1000)) / 1000)
    x_checksum = hashlib.md5(api_key + str(x_time) + x_param).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    req = urllib2.Request(url, body, x_header)
    result = urllib2.urlopen(req)
    result = json.loads(result.read())
    if result['code'] == '0':
        return [result['data']]
    raise Exception(result['desc'])