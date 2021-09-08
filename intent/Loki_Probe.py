#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for Probe

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict

    Output:
        resultDICT    dict
"""

DEBUG_Probe = True
userDefinedDICT = {"AZ": ["AZ", "AstraZeneca", "az", "牛津", "牛津/阿斯利康", "阿斯利康", "阿斯特捷利康"], "dose": ["第一劑", "第三劑", "第二劑"], "doze": ["第一劑", "第二劑", "第三劑"], "Taiwan": ["全台", "全台灣", "全國", "全島", "全臺", "全臺各地", "全臺灣", "台灣", "本國", "本島", "臺灣"], "Medigen": ["Medigen", "medigen", "高端"], "Moderna": ["Moderna", "莫德納"], "leftover": ["剩量", "剩餘", "剩餘分佈", "剩餘分布", "剩餘數", "剩餘數字", "剩餘資料", "剩餘量", "庫存"], "syn_verb": ["有", "出現"], "group_num": ["第一類", "第二類", "第三類", "第四類", "第五類", "第六類", "第七類", "第八類", "第九類", "第十類"], "side_effect": ["副作用", "嚴重副作用"], "vaccine_verb": ["注射", "接種", "打完", "打過"], "Pfizer-BioNTech": ["BIOTECH", "BNT", "BioTech", "Biotech", "Pfizer-BioNTech", "biotech", "上海復興", "上海復興BNT", "輝瑞"]}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_Probe:
        print("[Probe] {} ===> {}".format(inputSTR, utterance))

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    resultDICT["inquiry_type"] = []
    resultDICT["confirm"] = []
    if utterance == "[az]疫苗[剩餘量]":
        if args[1] in userDefinedDICT["leftover"]:
            resultDICT["inquiry_type"] = "leftover"
        elif args[1] in userDefinedDICT["side_effect"]:
            resultDICT["inquiry_type"] = "side_effect"

    if utterance == "[台北]還剩下多少[az]疫苗":
        if "剩下" in inputSTR:
            resultDICT["inquiry_type"] = "leftover"

    if utterance == "[台南]剩下多少疫苗":
        if "剩下" in inputSTR:
            resultDICT["inquiry_type"] = "leftover"

    if utterance == "[台南]疫苗[剩餘量]":
        if args[1] in userDefinedDICT["leftover"]:
            resultDICT["inquiry_type"] = "leftover"

    if utterance == "[我]想要知道疫苗資訊":
        resultDICT["msg"] = "想知道關於疫苗的哪些資訊呢? 如: 疫苗剩餘量、疫苗庫存量、疫苗副作用...等資訊"

    if utterance == "[疫苗][剩餘量]":
        if args[1] in userDefinedDICT["leftover"]:
            resultDICT["inquiry_type"] = "leftover"
        elif args[1] in userDefinedDICT["side_effect"]:
            resultDICT["inquiry_type"] = "side_effect"

    # if utterance == "不是":
    #     if len(inputSTR) < 3:
    #         resultDICT["confirm"] = False
    #     pass

    # if utterance == "是":
    #     if len(inputSTR) < 2:
    #         resultDICT["confirm"] = True
    #     pass

    return resultDICT 