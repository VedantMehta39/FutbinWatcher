from requests_html import HTMLSession
from bs4 import BeautifulSoup
import time
import json
import pandas as pd
from collections import defaultdict
import sys
import os
import random

def main():
    option = input("What do you want to do?\nA Track Investments \nB Receive Price Alerts \n\n")
    session = HTMLSession()
    if option.upper() == 'A':
        playersFile=os.path.dirname(sys.argv[0])+"/InvestmentManagement.txt"
        dict_table=parseFile(playersFile,session)
        pandasPlayerTable=pd.DataFrame(dict_table)
        pd.set_option('display.expand_frame_repr', False)
        print(pandasPlayerTable)


    elif option.upper()=='B':
        playersFile = os.path.dirname(sys.argv[0])+"/PriceAlert.txt"
        runtime=float(input("\nHow long do you want the app to keep running?(in minutes)\n"))
        eventName=input("\nPlease enter your ifttt event name\n")
        eventKey=input("\nPlease enter your ifttt event key\n")
        currentTime=time.time()
        while time.time()-currentTime<=(runtime*60):
            parseFile(playersFile,session, alert=True,eventName=eventName,eventKey=eventKey)
            time.sleep(15*60)
    else:
        print("Wrong option chosen. Closing script")
        sys.exit()

def parseFile(playersFile,session,**kwargs):
    players = open(playersFile, "r")
    dict_table=defaultdict(list)
    player = players.readline()
    playersAtTargetPrice={}
    if 'alert' in kwargs:
        while player:
            data = player.split()
            try:
                url = data[0]
                console=data[1]
                targetAlertPrice = float(data[2])
                player_name,livePrice=price_scrape(url,console,session)
                if livePrice<=targetAlertPrice:
                    playersAtTargetPrice["value1"] = player_name
                    playersAtTargetPrice["value2"]=livePrice
                alert(kwargs["eventName"], kwargs["eventKey"], playersAtTargetPrice, session)
            except :
                print("File Not Formatted Properly")
                sys.exit()
            time.sleep(random.randint(2,4))
            player = players.readline()
        players.close()
        return playersAtTargetPrice
    else:
        while player:
            data = player.split()
            try:
                url = data[0]
                costPrice = float(data[1])
                quantity = float(data[2])
                targetSellingPrice = float(data[3])
                console = data[4]
                player_name, livePrice = price_scrape(url, console,session)
                dict_table["Name"].append(player_name)
                dict_table["Cost Price"].append(costPrice)
                dict_table["Quantity"].append(quantity)
                dict_table["Total Cost"].append(costPrice * quantity)
                dict_table["Target Price"].append(targetSellingPrice)
                dict_table["Live Price"].append(livePrice)
                dict_table["Projected Profit/Loss"].append(0.95 * ((livePrice - costPrice) * quantity))
            except IndexError:
                print("File Not Formatted Properly")
                sys.exit()
            time.sleep(random.randint(2,4))
            player = players.readline()
        players.close()
        return dict_table

def price_scrape(url,console,session):
    r = session.get(url)
    soup = BeautifulSoup(r.content, "lxml")
    tagPrice = soup.find("div", id="page-info")
    tagName = soup.find("span", {"class": "header_name"})
    player_name = tagName.text
    player_id = tagPrice["data-player-resource"]
    prices = json.loads(session.get(url[:26]+"playerPrices?player=" + player_id).text)
    livePrice = float(prices[player_id]["prices"][console]["LCPrice"].replace(",", ""))
    r.close()
    return player_name, livePrice

def alert(eventName,eventKey,playersAtTargetPrice,session):
    session.post(f"https://maker.ifttt.com/trigger/{eventName}/with/key/{eventKey}",data=playersAtTargetPrice)

if __name__=="__main__":
    main()
