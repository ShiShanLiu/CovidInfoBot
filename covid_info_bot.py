#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki 2.0 Template For Python3

    [URL] https://api.droidtown.co/Loki/BulkAPI/

    Request:
        {
            "username": "your_username",
            "input_list": ["your_input_1", "your_input_2"],
            "loki_key": "your_loki_key",
            "filter_list": ["intent_filter_list"] # optional
        }

    Response:
        {
            "status": True,
            "msg": "Success!",
            "version": "v223",
            "word_count_balance": 2000,
            "result_list": [
                {
                    "status": True,
                    "msg": "Success!",
                    "results": [
                        {
                            "intent": "intentName",
                            "pattern": "matchPattern",
                            "utterance": "matchUtterance",
                            "argument": ["arg1", "arg2", ... "argN"]
                        },
                        ...
                    ]
                },
                {
                    "status": False,
                    "msg": "No Match Intent!"
                }
            ]
        }
"""

import re
from requests import post
from requests import codes
import math
import json
try:
    from intent import Loki_vaccine_stock
    from intent import Loki_side_effect
    from intent import Loki_Probe
    from intent import Loki_group
except:
    from .intent import Loki_vaccine_stock
    from .intent import Loki_side_effect
    from .intent import Loki_Probe
    from .intent import Loki_group

with open("account.info", mode="r", encoding="utf-8") as file:
    useraccountdict = json.loads(file.read())
LOKI_URL = "https://api.droidtown.co/Loki/BulkAPI/"
USERNAME = useraccountdict["username"]
LOKI_KEY = useraccountdict["loki_project_key"]
# 意圖過濾器說明
# INTENT_FILTER = []        => 比對全部的意圖 (預設)
# INTENT_FILTER = [intentN] => 僅比對 INTENT_FILTER 內的意圖
INTENT_FILTER = []

class LokiResult():
    status = False
    message = ""
    version = ""
    balance = -1
    lokiResultLIST = []

    def __init__(self, inputLIST, filterLIST):
        self.status = False
        self.message = ""
        self.version = ""
        self.balance = -1
        self.lokiResultLIST = []
        # filterLIST 空的就採用預設的 INTENT_FILTER
        if filterLIST == []:
            filterLIST = INTENT_FILTER

        try:
            result = post(LOKI_URL, json={
                "username": USERNAME,
                "input_list": inputLIST,
                "loki_key": LOKI_KEY,
                "filter_list": filterLIST
            })

            if result.status_code == codes.ok:
                result = result.json()
                self.status = result["status"]
                self.message = result["msg"]
                if result["status"]:
                    self.version = result["version"]
                    self.balance = result["word_count_balance"]
                    self.lokiResultLIST = result["result_list"]
            else:
                self.message = "Connect failed."
        except Exception as e:
            self.message = str(e)

    def getStatus(self):
        return self.status

    def getMessage(self):
        return self.message

    def getVersion(self):
        return self.version

    def getBalance(self):
        return self.balance

    def getLokiStatus(self, index):
        rst = False
        if index < len(self.lokiResultLIST):
            rst = self.lokiResultLIST[index]["status"]
        return rst

    def getLokiMessage(self, index):
        rst = ""
        if index < len(self.lokiResultLIST):
            rst = self.lokiResultLIST[index]["msg"]
        return rst

    def getLokiLen(self, index):
        rst = 0
        if index < len(self.lokiResultLIST):
            if self.lokiResultLIST[index]["status"]:
                rst = len(self.lokiResultLIST[index]["results"])
        return rst

    def getLokiResult(self, index, resultIndex):
        lokiResultDICT = None
        if resultIndex < self.getLokiLen(index):
            lokiResultDICT = self.lokiResultLIST[index]["results"][resultIndex]
        return lokiResultDICT

    def getIntent(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["intent"]
        return rst

    def getPattern(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["pattern"]
        return rst

    def getUtterance(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["utterance"]
        return rst

    def getArgs(self, index, resultIndex):
        rst = []
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["argument"]
        return rst

def runLoki(inputLIST, filterLIST=[]):
    resultDICT = {}
    lokiRst = LokiResult(inputLIST, filterLIST)
    if lokiRst.getStatus():
        for index, key in enumerate(inputLIST):
            for resultIndex in range(0, lokiRst.getLokiLen(index)):
                # vaccine_stock
                if lokiRst.getIntent(index, resultIndex) == "vaccine_stock":
                    resultDICT = Loki_vaccine_stock.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # side_effect
                if lokiRst.getIntent(index, resultIndex) == "side_effect":
                    resultDICT = Loki_side_effect.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Probe
                if lokiRst.getIntent(index, resultIndex) == "Probe":
                    resultDICT = Loki_Probe.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # group
                if lokiRst.getIntent(index, resultIndex) == "group":
                    resultDICT = Loki_group.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

    else:
        resultDICT = {"msg": lokiRst.getMessage()}
    return resultDICT

def testLoki(inputLIST, filterLIST):
    INPUT_LIMIT = 20
    for i in range(0, math.ceil(len(inputLIST) / INPUT_LIMIT)):
        resultDICT = runLoki(inputLIST[i*INPUT_LIMIT:(i+1)*INPUT_LIMIT], filterLIST)


if __name__ == "__main__":
    # vaccine_stock
    # print("[TEST] vaccine_stock")
    # inputLIST = ['台中剩下多少疫苗','台中剩下多少AZ疫苗','台中剩下多少劑疫苗','台北還有幾劑疫苗？','給我全台疫苗剩餘數','台中剩下多少劑AZ疫苗','台北還有幾劑AZ疫苗？','給我全台AZ疫苗剩餘數','能給我全台疫苗剩餘數','能給我全台AZ疫苗剩餘數','我想查詢台北疫苗剩餘量','我想知道台北疫苗剩餘量','我要查詢台北疫苗剩餘量','我要知道台北疫苗剩餘量','幫我查詢AZ在台北的剩餘量','我想知道AZ在台北的剩餘量','我要查詢AZ在台北的剩餘量','我想知道全臺疫苗剩餘分佈','可以幫我查詢AZ在台北的剩餘量','幫我查詢AZ疫苗在台北的剩餘量','我想知道AZ疫苗在台北的剩餘量','我想知道全臺高端疫苗剩餘分佈','可以跟我講台北疫苗剩下多少嗎？','可以幫我查詢AZ疫苗在台北的剩餘量']
    # testLoki(inputLIST, ['vaccine_stock'])
    # print("")

    # side_effect
    # print("[TEST] side_effect")
    # inputLIST = ['az副作用','第一劑az副作用','az疫苗副作用為何','第一劑az疫苗副作用','請問az疫苗副作用為何','第一劑az會有哪些副作用','第一劑az疫苗會有哪些副作用','打完莫德納後，出現哪些嚴重副作用需要送醫','打完莫德納疫苗後，出現哪些嚴重副作用需要送醫']
    # testLoki(inputLIST, ['side_effect'])
    # print("")

    # Probe
    # print("[TEST] Probe")
    # inputLIST = ['是','不是','疫苗剩餘量','az疫苗剩餘量','台南疫苗剩餘量','台南剩下多少疫苗','我想要知道疫苗資訊','台北還剩下多少az疫苗']
    # testLoki(inputLIST, ['Probe'])
    # print("")

    # group
    # print("[TEST] group")
    # inputLIST = ['第一類族群','第一類接種對象']
    # testLoki(inputLIST, ['group'])
    # print("")

    # 輸入其它句子試看看


    inputLIST = ["az副作用"]
    filterLIST = []
    resultDICT = runLoki(inputLIST, filterLIST)
    print(" ")
    # for i in resultDICT:
    #     if resultDICT[i] != None:
    #         print(resultDICT[i])
    #     else:
    #         pass
    inputLIST = ["我想知道az副作用"]
    print(resultDICT)
    # print("Result => {}".format(resultDICT))