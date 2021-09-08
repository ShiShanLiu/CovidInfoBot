#!/user/bin/env python
# -*- coding: utf-8 -*-

import logging #可以測試哪裡有問題
import discord
import json
import re
from covid_info_bot import runLoki

import vaccine_stock_api
from pprint import pprint


logging.basicConfig(level=logging.CRITICAL)

# <取得多輪對話資訊>
client = discord.Client()

sideEffectTemplate ={
                "vaccine_shot":"",
                 "side_effect": "",
                 "side_effect_var":""
                 }
severeSideEffectTemplate = {
    "vaccine_shot" : "",
    "severe_side_effect" : ""
}

vaccineStockTemplate = {
                "vaccine_shot":"",
                "location":"",
                "vaccine_stock":""
                }

mscDICT = {
    # "userID": {side_effectTemplate, vaccine_stockTemplate, severeSideEffectTemplate}
}
# </取得多輪對話資訊>

with open("account.info", encoding="utf-8") as f:
    accountDICT = json.loads(f.read())
# 另一個寫法是：accountDICT = json.load(open("account.info", encoding="utf-8"))


punctuationPat = re.compile("[,\.\?:;，。？、：；\n]+")

def getLokiResult(inputSTR):
    punctuationPat = re.compile("[,\.\?:;，。？、：；\n]+")
    inputLIST = punctuationPat.sub("\n", inputSTR).split("\n")
    filterLIST = []
    resultDICT = runLoki(inputLIST, filterLIST)
    print("Loki Result => {}".format(resultDICT))
    return resultDICT



@client.event
async def on_ready():
    logging.info("[READY INFO] {} has connected to Discord!".format(client.user))
    print("[READY INFO] {} has connected to Discord!".format(client.user))


@client.event
async def on_message(message):
    # if message.channel.name != "dt_intern":
    #     return

    if not re.search("<@[!&]{}> ?".format(client.user.id), message.content):    # 只有 @Bot 才會回應
        return

    if message.author == client.user:
        return

# try:
    print("client.user.id =", client.user.id, "\nmessage.content =", message.content)
    msgSTR = re.sub("<@[!&]{}> ?".format(client.user.id), "", message.content)    # 收到 User 的訊息，將 id 取代成 ""
    print("msgSTR =", msgSTR)
    replySTR = ""    # Bot 回應訊息

    if re.search("(hi|hello|哈囉|嗨|[你您]好)", msgSTR.lower()):
        replySTR = "Hi 您好，想知道哪些疫苗資訊呢?"
        await message.reply(replySTR)
        return

    lokiResultDICT = getLokiResult(msgSTR)    # 取得 Loki 回傳結果
    if lokiResultDICT:
        if client.user.id not in mscDICT:    # 判斷 User 是否為第一輪對話
            mscDICT[client.user.id] = { 
                                        "side_effect": {},
                                        "vaccine_stock": {},
                                        "inquiry_type": {},
                                        "completed": False}

        for k in lokiResultDICT:    # 將 Loki Intent 的結果，存進 Global mscDICT 變數，可替換成 Database。
            """
            lokiResultDICT = {"vaccine_shot"=[AZ, Moderna],"severe_side_effect"=['注射部位','注射部位']}

            在 for c in lokiResultDICT迴圈裡面：
            mscDICT[client.user.id]["side_effect"]["side_effect"] = ['注射部位','注射部位']
            """
            if k == "inquiry_type":
                mscDICT[client.user.id]["inquiry_type"] = lokiResultDICT["inquiry_type"]

            if k == "side_effect_var":
                for c in lokiResultDICT:
                    mscDICT[client.user.id]["side_effect"][c] = lokiResultDICT[c]
                    mscDICT[client.user.id]["inquiry_type"] = "side_effect"

            elif k == "vaccine_stock":
                for c in lokiResultDICT:
                    mscDICT[client.user.id]["vaccine_stock"][c] = lokiResultDICT[c]
                    mscDICT[client.user.id]["inquiry_type"] = "vaccine_stock"

            # elif k == "confirm":
            #     if lokiResultDICT["confirm"]:
            #         replySTR = "好的，謝謝。"
            #     else:
            #         replySTR = "請問您的意思是？"

        ### inquiry_type 多輪對話的問句 ###
        if mscDICT[client.user.id]["inquiry_type"] == {} and replySTR == "":    
            replySTR = '\n請問要問關於疫苗的甚麼資訊呢？'

        ### side_effect 多輪對話的問句 ###
        if mscDICT[client.user.id]["inquiry_type"] == "side_effect" and replySTR == "":   
            if "vaccine_shot" not in mscDICT[client.user.id]["side_effect"]:
                replySTR = "請問您想知道哪個廠牌的疫苗資訊？"
            # elif "location" not in mscDICT[client.user.id]["side_effect"]:
            #     replySTR = "請問您要詢問哪個地區的[{}]疫苗庫存呢？".format(mscDICT[client.user.id]["vaccine_stock"]["vaccine_shot"])          

        ### vaccine_stock 多輪對話的問句 ###
        if mscDICT[client.user.id]["inquiry_type"] == "vaccine_stock" and replySTR == "":
            if "vaccine_shot" not in mscDICT[client.user.id]["vaccine_stock"]:
                replySTR = "請問您想知道哪個廠牌的疫苗資訊？"
            elif "location" not in mscDICT[client.user.id]["vaccine_stock"]:
                replySTR = "請問您要詢問哪個地區的{}疫苗庫存呢？"

        ### side_effect 確認 ###
        if set(sideEffectTemplate.keys()).difference(mscDICT[client.user.id]["side_effect"]) == set() and replySTR == "":
            for i in range(len(mscDICT[client.user.id]["side_effect"]["vaccine_shot"])):
                if mscDICT[client.user.id]["side_effect"]["side_effect"]:
                    replySTR += """{}疫苗的常見副作用是{}。\n""".format(mscDICT[client.user.id]["side_effect"]["vaccine_shot"][i],
                                                                    mscDICT[client.user.id]["side_effect"]["side_effect"][i])
                if mscDICT[client.user.id]["side_effect"]["severe_side_effect"]:
                    replySTR += """{}疫苗的常見副作用是{}。\n""".format(mscDICT[client.user.id]["side_effect"]["vaccine_shot"][i],
                                                                    mscDICT[client.user.id]["side_effect"]["severe_side_effect"][i])

            mscDICT[client.user.id]["completed"] = True

        ### vaccine_stock 確認 ###
        if set(vaccineStockTemplate.keys()).difference(mscDICT[client.user.id]["vaccine_stock"]) == set() and replySTR == "":
            replySTR = vaccine_stock_api.write_response(mscDICT[client.user.id]["vaccine_stock"])
            mscDICT[client.user.id]["completed"] = True

    print("mscDICT =")
    pprint(mscDICT)

    if mscDICT[client.user.id]["completed"]:    # 清空 User Dict
        del mscDICT[client.user.id]

    if replySTR:    # 回應 User 訊息
        await message.reply(replySTR)
    return

# except Exception as e:
    logging.error("[MSG ERROR] {}".format(str(e)))
    print("[MSG ERROR] {}".format(str(e)))


if __name__ == "__main__":
    client.run(accountDICT["discord_token"])