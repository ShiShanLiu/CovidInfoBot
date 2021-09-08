#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for vaccine_stock

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict

    Output:
        resultDICT    dict
"""

import json

DEBUG_vaccine_stock = True
userDefinedDICT = {"AZ": ["AZ", "AstraZeneca", "az", "牛津", "牛津/阿斯利康", "阿斯利康", "阿斯特捷利康"], "dose": ["第一劑", "第三劑", "第二劑"], "doze": ["第一劑", "第二劑", "第三劑"], "Taiwan": ["全台", "全台灣", "全國", "全島", "全臺", "全臺各地", "全臺灣", "台灣", "本國", "本島", "臺灣"], "Medigen": ["Medigen", "medigen", "高端"], "Moderna": ["Moderna", "莫德納"], "leftover": ["剩量", "剩餘", "剩餘分佈", "剩餘分布", "剩餘數", "剩餘數字", "剩餘資料", "剩餘量","庫存"], "syn_verb": ["有", "出現"], "group_num": ["第一類", "第二類", "第三類", "第四類", "第五類", "第六類", "第七類", "第八類", "第九類", "第十類"], "side_effect": ["副作用", "嚴重副作用"], "vaccine_verb": ["注射", "接種", "打完", "打過"], "Pfizer-BioNTech": ["BIOTECH", "BNT", "BioTech", "Biotech", "Pfizer-BioNTech", "biotech", "上海復興", "上海復興BNT", "輝瑞"]}
vaccineDICT = userDefinedDICT["AZ"] + userDefinedDICT["Moderna"] + userDefinedDICT["Pfizer-BioNTech"] + userDefinedDICT["Medigen"]
locationDICT = json.loads(open("json/taiwan_location_name.json", mode="r", encoding="utf-8").read()) 
locationDICT['Taiwan'] = userDefinedDICT["Taiwan"]
allLocationLIST = []
for i in locationDICT.values():
    allLocationLIST += i

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_vaccine_stock:
        print("[vaccine_stock] {} ===> {}".format(inputSTR, utterance))

def formalize_name(val, userDefinedDICT, resultDICT, resultSTR):
    '''
    Formalizes the name of user defined words.
    val (str): value from agrs
    userDefinedDICT (dict): user defined dict
    resultDICT (dict): result dict
    resultSTR (str): key of result dict
    '''
    count = 0
    for k in userDefinedDICT.keys():
        if val in userDefinedDICT[k]:
            if count == 0: resultDICT[resultSTR].append(k); count+=1
            if count > 1: print(f"Name Error: Duplicate Names! ({val})")

        count = 0

# def getlocationname(val, locationDICT, resultDICT, resultSTR):
#     for k in locationDICT.keys():
#         if val in locationDICT[k]:
#             resultDICT[resultSTR].append(k)

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    if resultDICT == {}:
        resultDICT['vaccine_shot'] = []
        resultDICT['location'] = []

    if utterance == "[可以]幫[我]查詢[AZ]在[台北]的[剩餘量]":
        if args[4] in userDefinedDICT['leftover']:
            if args[2] in vaccineDICT: formalize_name(args[2], userDefinedDICT, resultDICT, 'vaccine_shot')
            if args[3] in allLocationLIST: formalize_name(args[3], locationDICT, resultDICT, 'location')
            # if args[3] in locationDICT:
            #     getlocationname(args[3], locationDICT, resultDICT, "location")


    if utterance == "[可以]幫[我]查詢[AZ]疫苗在[台北]的[剩餘量]":
        if args[4] in userDefinedDICT['leftover']:
            if args[2] in vaccineDICT: formalize_name(args[2], userDefinedDICT, resultDICT, "vaccine_shot")
            if args[3] in allLocationLIST: formalize_name(args[3], locationDICT, resultDICT, 'location')
            # if args[3] in locationDICT:
            #     getlocationname(args[3], locationDICT, resultDICT, "location")

    if utterance == "[可以]跟[我]講[台北]疫苗剩下多少嗎？":
        resultDICT['vaccine_shot'].append('all')
        if args[2] in allLocationLIST: formalize_name(args[2], locationDICT, resultDICT, 'location')
        # if args[2] in locationDICT:
        #         getlocationname(args[2], locationDICT, resultDICT, "location")

    if utterance == "[台中]剩下多少[AZ]疫苗":
        if args[1] in vaccineDICT: formalize_name(args[1], userDefinedDICT, resultDICT, "vaccine_shot")
        if args[0] in allLocationLIST: formalize_name(args[0], locationDICT, resultDICT, 'location')
        # if args[0] in locationDICT:
        #         getlocationname(args[0], locationDICT, resultDICT, "location")


    if utterance == "[台中]剩下多少[劑][AZ]疫苗":
        if args[2] in vaccineDICT: formalize_name(args[2], userDefinedDICT, resultDICT, "vaccine_shot")
        if args[0] in allLocationLIST: formalize_name(args[0], locationDICT, resultDICT, 'location')
        # if args[0] in locationDICT:
        #         getlocationname(args[0], locationDICT, resultDICT, "location")

    if utterance == "[台中]剩下多少[劑]疫苗":
        resultDICT['vaccine_shot'].append('all')
        if args[0] in locatallLocationLISTionDICT: formalize_name(args[0], locationDICT, resultDICT, 'location')
        # if args[0] in locationDICT:
        #         getlocationname(args[0], locationDICT, resultDICT, "location")

    if utterance == "[台中]剩下多少疫苗":
        resultDICT['vaccine_shot'].append('all')
        if args[0] in allLocationLIST: formalize_name(args[0], locationDICT, resultDICT, 'location')
        # if args[0] in locationDICT:
        #         getlocationname(args[0], locationDICT, resultDICT, "location")

    if utterance == "[台北]還有幾[劑][AZ]疫苗？":
        if args[2] in vaccineDICT: formalize_name(args[2], userDefinedDICT, resultDICT, "vaccine_shot")
        if args[0] in allLocationLIST: formalize_name(args[0], locationDICT, resultDICT, 'location')
        # if args[0] in locationDICT:
        #         getlocationname(args[0], locationDICT, resultDICT, "location")

    if utterance == "[台北]還有幾[劑]疫苗？":
        resultDICT['vaccine_shot'].append('all')
        if args[0] in allLocationLIST: formalize_name(args[0], locationDICT, resultDICT, 'location')
        # if args[0] in locationDICT:
        #         getlocationname(args[0], locationDICT, resultDICT, "location")

    if utterance == "[我]想查詢[台北]疫苗[剩餘量]":
        if args[2] in userDefinedDICT['leftover']:
            resultDICT['vaccine_shot'].append('all')
        if args[1] in allLocationLIST: formalize_name(args[1], locationDICT, resultDICT, 'location')
            # if args[1] in locationDICT:
            #     getlocationname(args[1], locationDICT, resultDICT, "location")

    if utterance == "[我]想知道[AZ]在[台北]的[剩餘量]":
        if args[3] in userDefinedDICT['leftover']:
            if args[1] in vaccineDICT: formalize_name(args[1], userDefinedDICT, resultDICT, "vaccine_shot")
            if args[2] in allLocationLIST: formalize_name(args[2], locationDICT, resultDICT, 'location')
            # if args[2] in locationDICT:
            #     getlocationname(args[2], locationDICT, resultDICT, "location")

    if utterance == "[我]想知道[AZ]疫苗在[台北]的[剩餘量]":
        if args[3] in userDefinedDICT['leftover']:
            if args[1] in vaccineDICT: formalize_name(args[1], userDefinedDICT, resultDICT, "vaccine_shot")
            if args[2] in allLocationLIST: formalize_name(args[2], locationDICT, resultDICT, 'location')
            # if args[2] in locationDICT:
            #     getlocationname(args[2], locationDICT, resultDICT, "location")

    if utterance == "[我]想知道[全臺][高端]疫苗[剩餘分佈]":
        if args[3] in userDefinedDICT['leftover']:
            if args[2] in vaccineDICT: formalize_name(args[2], userDefinedDICT, resultDICT, "vaccine_shot")
            if args[1] in allLocationLIST: formalize_name(args[1], locationDICT, resultDICT, 'location')

    if utterance == "[我]想知道[全臺]疫苗[剩餘分佈]":
        if args[2] in userDefinedDICT['leftover']:
            resultDICT['vaccine_shot'].append('all')
            if args[1] in allLocationLIST: formalize_name(args[1], locationDICT, resultDICT, 'location')

    if utterance == "[我]想知道[台北]疫苗[剩餘量]":
        if args[2] in userDefinedDICT['leftover']:
            resultDICT['vaccine_shot'].append('all')
            if args[1] in allLocationLIST: formalize_name(args[1], locationDICT, resultDICT, 'location')
            # if args[1] in locationDICT:
            #     getlocationname(args[1], locationDICT, resultDICT, "location")

    if utterance == "[我]要查詢[AZ]在[台北]的[剩餘量]":
        if args[3] in userDefinedDICT['leftover']:
            print()
            if args[1] in vaccineDICT: formalize_name(args[1], userDefinedDICT, resultDICT, "vaccine_shot")
            if args[2] in allLocationLIST: formalize_name(args[2], locationDICT, resultDICT, 'location')
            # if args[2] in locationDICT:
            #     getlocationname(args[2], locationDICT, resultDICT, "location")

    if utterance == "[我]要查詢[台北]疫苗[剩餘量]":
        if args[2] in userDefinedDICT['leftover']:
            resultDICT['vaccine_shot'].append('all')
            if args[1] in allLocationLIST: formalize_name(args[1], locationDICT, resultDICT, 'location')
            # if args[1] in locationDICT:
            #     getlocationname(args[1], locationDICT, resultDICT, "location")

    if utterance == "[我]要知道[台北]疫苗[剩餘量]":
        if args[2] in userDefinedDICT['leftover']:
            resultDICT['vaccine_shot'].append('all')
            if args[1] in allLocationLIST: formalize_name(args[1], locationDICT, resultDICT, 'location')
            # if args[1] in locationDICT:
            #     getlocationname(args[1], locationDICT, resultDICT, "location")


    if utterance == "[能]給[我][全台][AZ]疫苗[剩餘數]":
        if args[4] in userDefinedDICT['leftover']:
            if args[3] in vaccineDICT: formalize_name(args[3], userDefinedDICT, resultDICT, "vaccine_shot")
            if args[2] in allLocationLIST: formalize_name(args[2], locationDICT, resultDICT, 'location')


    if utterance == "[能]給[我][全台]疫苗[剩餘數]":
        if args[3] in userDefinedDICT['leftover']:
            resultDICT['vaccine_shot'].append('all')
            if args[2] in allLocationLIST: formalize_name(args[2], locationDICT, resultDICT, 'location')

    if utterance == "幫[我]查詢[AZ]在[台北]的[剩餘量]":
        if args[3] in userDefinedDICT['leftover']:
            if args[1] in vaccineDICT: formalize_name(args[1], userDefinedDICT, resultDICT, "vaccine_shot")
            if args[2] in allLocationLIST: formalize_name(args[2], locationDICT, resultDICT, 'location')
            # if args[2] in locationDICT:
            #     getlocationname(args[2], locationDICT, resultDICT, "location")

    if utterance == "幫[我]查詢[AZ]疫苗在[台北]的[剩餘量]":
        if args[3] in userDefinedDICT['leftover']:
            if args[1] in vaccineDICT: formalize_name(args[1], userDefinedDICT, resultDICT, "vaccine_shot")
            if args[2] in allLocationLIST: formalize_name(args[2], locationDICT, resultDICT, 'location')
            # if args[2] in locationDICT:
            #     getlocationname(args[2], locationDICT, resultDICT, "location")

    if utterance == "給[我][全台][AZ]疫苗[剩餘數]":
        if args[3] in userDefinedDICT['leftover']:
            if args[2] in vaccineDICT: formalize_name(args[2], userDefinedDICT, resultDICT, "vaccine_shot")
            # if args[1] in locationDICT: formalize_name(args[1], userDefinedDICT, resultDICT, 'location')

    if utterance == "給[我][全台]疫苗[剩餘數]":
        if args[2] in userDefinedDICT['leftover']:
            resultDICT['vaccine_shot'].append('all')
            # if args[1] in locationDICT: formalize_name(args[1], userDefinedDICT, resultDICT, 'location')
            
    resultDICT["vaccine_stock"] = []

    return resultDICT