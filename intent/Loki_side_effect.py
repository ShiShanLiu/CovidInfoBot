#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for side_effect
    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict
    Output:
        resultDICT    dict
"""

import json

with open("json/side_effect.json", mode="r", encoding="utf-8") as file:
    sideeffectDICT = json.loads(file.read())

with open("json/hospital_immediately.json", mode="r", encoding="utf-8") as f:
    hospitalDICT = json.loads(f.read())

DEBUG_side_effect = True
userDefinedDICT = {"AZ": ["AZ", "AstraZeneca", "az", "牛津", "牛津/阿斯利康", "阿斯利康", "阿斯特捷利康"], "dose": ["第一劑", "第三劑", "第二劑"], "doze": ["第一劑", "第二劑", "第三劑"], "Taiwan": ["全台", "全台灣", "全國", "全島", "全臺", "全臺各地", "全臺灣", "台灣", "本國", "本島", "臺灣"], "Medigen": ["Medigen", "medigen", "高端"], "Moderna": ["Moderna", "莫德納"], "leftover": ["剩量", "剩餘", "剩餘分佈", "剩餘分布", "剩餘數", "剩餘數字", "剩餘資料", "剩餘量","庫存"], "syn_verb": ["有", "出現"], "group_num": ["第一類", "第二類", "第三類", "第四類", "第五類", "第六類", "第七類", "第八類", "第九類", "第十類"], "side_effect": ["副作用", "嚴重副作用"], "vaccine_verb": ["注射", "接種", "打完", "打過"], "Pfizer-BioNTech": ["BIOTECH", "BNT", "BioTech", "Biotech", "Pfizer-BioNTech", "biotech", "上海復興", "上海復興BNT", "輝瑞"]}
vaccineDICT = userDefinedDICT["AZ"] + userDefinedDICT["Moderna"] + userDefinedDICT["Pfizer-BioNTech"] + userDefinedDICT["Medigen"]

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_side_effect:
        print("[side_effect] {} ===> {}".format(inputSTR, utterance))

def formalize_name_side_effect(val, resultDICT, resultSTR, resultSTR2):
    count = 0
    for k in userDefinedDICT.keys():
        if val in userDefinedDICT[k]:
            if count == 0: 
                resultDICT[resultSTR].append(k)
                side_effect = sideeffectDICT[k]
                resultDICT[resultSTR2].append(side_effect)
                count+=1
            if count > 1: 
                print(f"Name Error: Duplicate Names! ({val})")

def formalize_name_severe_side_effect(val, resultDICT, resultSTR, resultSTR2):
    count = 0
    for k in userDefinedDICT.keys():
        if val in userDefinedDICT[k]:
            if count == 0: 
                resultDICT[resultSTR].append(k)
                severe_side_effect= hospitalDICT[k]
                print(resultDICT)
                resultDICT[resultSTR2].append(severe_side_effect)
                count+=1
            if count > 1: 
                print(f"Name Error: Duplicate Names! ({val})")


def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    if resultDICT == {}:
        resultDICT["vaccine_shot"] = []
        resultDICT["side_effect"] = []
        resultDICT["severe_side_effect"] = []

    if utterance == "[az]疫苗[副作用]":
        if args[0] in vaccineDICT and args[1] == "副作用":
            formalize_name_side_effect(args[0], resultDICT, "vaccine_shot", "side_effect")
        elif args[0] in vaccineDICT and args[1] == "嚴重副作用":
            formalize_name_severe_side_effect(args[0], resultDICT, "vaccine_shot", "severe_side_effect")
        else:
            pass

    if utterance == "[az][副作用]":
        if args[0] in vaccineDICT and args[1] == "副作用":
            formalize_name_side_effect(args[0], resultDICT, "vaccine_shot", "side_effect")
        elif args[0] in vaccineDICT and args[1] == "嚴重副作用":
            formalize_name_severe_side_effect(args[0], resultDICT, "vaccine_shot", "severe_side_effect")
        else:
            pass

    if utterance == "[az]疫苗[會]有哪些[副作用]":
        if args[0] in vaccineDICT and args[2] == "副作用":
            formalize_name_side_effect(args[0], resultDICT, "vaccine_shot", "side_effect")
        else:
            pass

    if utterance == "[打完][莫德納][後]，[出現]哪些[嚴重副作用]需要送醫":
        if args[1] in vaccineDICT and args[4] == "嚴重副作用":
            formalize_name_severe_side_effect(args[1], resultDICT, "vaccine_shot", "severe_side_effect")
        else:
            pass

    if utterance == "[打完][莫德納]疫苗[後]，[出現]哪些[嚴重副作用]需要送醫":
        if args[1] in vaccineDICT and args[4] == "嚴重副作用":
            formalize_name_severe_side_effect(args[1], resultDICT, "vaccine_shot", "severe_side_effect")
        else:
            pass

    if utterance == "[第一劑][az][會]有哪些[副作用]":
        if args[1] in vaccineDICT and args[3] == "副作用":
            formalize_name_side_effect(args[1], resultDICT, "vaccine_shot", "side_effect")
        else:
            pass

    if utterance == "[第一劑][az][副作用]":
        if args[1] in vaccineDICT and args[2] == "副作用":
            formalize_name_side_effect(args[1], resultDICT, "vaccine_shot", "side_effect")
        else:
            pass

    if utterance == "[第一劑][az]疫苗[會][有]哪些[副作用]":
        if args[1] in vaccineDICT and args[4] == "副作用":
            formalize_name_side_effect(args[1], resultDICT, "vaccine_shot", "side_effect")
        else:
            pass

    if utterance == "[第一劑][az]疫苗[副作用]":
        if args[1] in vaccineDICT and args[2]:
            formalize_name_side_effect(args[1], resultDICT, "vaccine_shot", "side_effect")
        else:
            pass

    if utterance == "請問[az]疫苗[副作用]為何":
        if args[0] in vaccineDICT and args[1] == "副作用":
            formalize_name_side_effect(args[0], resultDICT, "vaccine_shot", "side_effect")
        else:
            pass

    if utterance == "[第一劑][az][會]有哪些[副作用]":
        if args[1] in vaccineDICT and args[3] == "副作用":
            formalize_name_side_effect(args[1], resultDICT, "vaccine_shot", "side_effect")
        else:
            pass
            
    if utterance == "[第一劑][az]疫苗[會]有哪些[副作用]":
        if args[1] in vaccineDICT and args[3] == "副作用":
            formalize_name_side_effect(args[1], resultDICT, "vaccine_shot", "side_effect")
        else:
            pass
    resultDICT["side_effect_var"] = []
    return resultDICT