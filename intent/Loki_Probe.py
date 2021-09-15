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
userDefinedDICT = {"AZ": ["AZ", "AstraZeneca", "az", "牛津", "牛津/阿斯利康", "阿斯利康", "阿斯特捷利康"], "Taiwan": ["全台", "全台灣", "全國", "全島", "全臺", "全臺各地", "全臺灣", "台灣", "本國", "本島", "臺灣"], "severe": ["嚴重"], "Medigen": ["Medigen", "medigen", "高端"], "Moderna": ["Moderna", "莫德納"], "leftover": ["剩量", "剩餘", "剩餘分佈", "剩餘分布", "剩餘數", "剩餘數字", "剩餘資料", "剩餘量"], "syn_verb": ["有", "出現"], "group_num": ["第一類", "第二類", "第三類", "第四類", "第五類", "第六類", "第七類", "第八類", "第九類", "第十類"], "第一劑": ["第 1 劑", "第1劑", "第 1劑", "第1 劑", "第１劑"], "第二劑": ["第 2 劑", "第2劑", "第 2劑", "第2 劑", "第２劑"], "information": ["資訊", "最新資訊"], "side_effect": ["副作用"], "updated_info": ["最新", "目前"], "vaccine_verb": ["注射", "接種", "打完", "打過"], "Pfizer-BioNTech": ["BIOTECH", "BNT", "BioTech", "Biotech", "Pfizer-BioNTech", "biotech", "上海復興", "上海復興BNT", "輝瑞", "bnt"]}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_Probe:
        print("[Probe] {} ===> {}".format(inputSTR, utterance))

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    # resultDICT["inquiry_type"] = []

    if utterance == "[我]想要知道疫苗[資訊]":
        resultDICT["msg"] = "想知道關於疫苗的哪些資訊呢? 如: 疫苗剩餘量、疫苗庫存量、疫苗副作用...等資訊"
    
    if utterance == "[我]想要知道[最新]疫苗資訊":
        resultDICT["msg"] = "想知道哪些最新疫苗資訊呢?"

    return resultDICT 