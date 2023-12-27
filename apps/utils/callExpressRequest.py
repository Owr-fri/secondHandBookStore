import time
import uuid
import requests
import hashlib
import base64
import ast
import urllib
import json

partnerID = 'PHClANGZZ'  # 此处替换为您在丰桥平台获取的顾客编码!
checkword = 'PbKYry97kCqIOBXDbFtVXgpXq5N23sNp'  # 此处替换为您在丰桥平台获取的校验码!

reqURL = 'https://sfapi-sbox.sf-express.com/std/service'


def getShippingCost(msgData):
    requestID = uuid.uuid1()  # 生成uuid

    timestamp = str(int(time.time()))  # 获取时间戳

    serviceCode = "FOP_RECE_QUERY_AGING_AND_FEE"

    def callSfExpressServiceByCSIM(reqURL, partnerID, requestID, serviceCode, timestamp, msgData, checkword):
        str = urllib.parse.quote_plus(msgData + timestamp + checkword)
        # 先md5加密然后base64加密
        m = hashlib.md5()
        m.update(str.encode('utf-8'))
        md5Str = m.digest()
        msgDigest = base64.b64encode(md5Str).decode('utf-8')
        data = {"partnerID": partnerID, "requestID": requestID, "serviceCode": serviceCode, "timestamp": timestamp,
                "msgDigest": msgDigest, "msgData": msgData}
        # 发送post请求
        res = requests.post(reqURL, data=data)
        return res.json()

    print('请求报文：' + msgData)
    respJson = callSfExpressServiceByCSIM(reqURL, partnerID, requestID, serviceCode, timestamp, msgData, checkword)
    if respJson != '':
        return respJson
