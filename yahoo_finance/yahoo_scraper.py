import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pickle
import numpy as np
import json

import re
from collections import OrderedDict
from time import strptime

import sys

import datetime;

# list of dictionary
main = []

# Initializing data Frame
df = pd.DataFrame()

driver = webdriver.Chrome(executable_path=r"chromedriver.exe")
driver.get('https://finance.yahoo.com/quote/%5EDJI')


# reading csv
symbol_lists = pd.read_csv('symbol_lists.csv')


for symbol in symbol_lists['Symbol']:
    print("\nSYMBOL \n",symbol)
    driver.get(f'https://finance.yahoo.com/quote/{symbol}')
    
    if '^' in symbol:
        print("\n Its a INDEX \n", symbol)
        
        #INDEX
        try:
            name = driver.find_element_by_xpath('//*[@id="quote-header-info"]/div[2]/div[1]/div[1]').text
        except:
            name = 'none'

        try:
            current = driver.find_element_by_xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/fin-streamer[1]').text
        except:
            current = 'none'

        try:
            change = driver.find_element_by_xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/fin-streamer[2]/span').text
        except:
            change = 'none'

        try:
            change_percentage = driver.find_element_by_xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/fin-streamer[3]/span').text.replace('(','').replace(')','')
        except:
            change_percentage = "none"

        try:
            previous_close = driver.find_element_by_xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[1]/td[2]').text
        except:
            previous_close = "none"

        try:
            Open = driver.find_element_by_xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[2]/td[2]').text
        except:
            Open = "none"

        try:
            volume = driver.find_element_by_xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[3]/td[2]').text
        except:
            volume = "none"

        try:
            day_range_min = driver.find_element_by_xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[1]/td[2]').text.split('-')[0]
        except:
            day_range_min = "none"

        try:
            day_range_max = driver.find_element_by_xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[1]/td[2]').text.split('-')[1]
        except:
            day_range_max = "none"

        try:
            _52_week_range_min = driver.find_element_by_xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[2]/td[2]').text.split('-')[0]
        except:
            _52_week_range_min = "none"

        try:
            _52_week_range_max = driver.find_element_by_xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[2]/td[2]').text.split('-')[1]
        except:
            _52_week_range_max = "none"

        try:
            avg_volume = driver.find_element_by_xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[3]/td[2]').text
        except:
            avg_volume = "none"

        timestamp = datetime.datetime.now()


        #making dictonary
        data = {
            'symbol':symbol,
            'name':name,
            'current':current.replace(",",""),
            'change':change,
            'change_percentage': change_percentage,
            'previous_close':previous_close.replace(",",""),
            'open':Open.replace(",",""),
            'volume':volume.replace(",",""),
            'day_range_min':day_range_min.replace(",",""),
            'day_range_max': day_range_max.replace(",",""),
            '52_week_range_min':_52_week_range_min.replace(",",""),
            '52_week_range_max': _52_week_range_max.replace(",",""),
            'avg_volume': avg_volume.replace(",",""),
            'timestamp':str(timestamp)
         }


        #append it to main data
        main.append(data)
        print("Making JSON")
        #Open and save in json file
        with open("demo.json", 'w', encoding="utf-8") as f:
                  json.dump(main, f,indent=4, ensure_ascii=False)


        #creating dataframe
        df = df.append({
            'symbol':symbol,
            'name':name,
            'current':current.replace(",",""),
            'change':change,
            'change_percentage': change_percentage,
            'previous_close':previous_close.replace(",",""),
            'open':Open.replace(",",""),
            'volume':volume.replace(",",""),
            'day_range_min':day_range_min.replace(",",""),
            'day_range_max': day_range_max.replace(",",""),
            '52_week_range_min':_52_week_range_min.replace(",",""),
            '52_week_range_max': _52_week_range_max.replace(",",""),
            'avg_volume': avg_volume.replace(",",""),
            'timestamp':str(timestamp)
         }, ignore_index=True)

        print("Making csv")
        df.to_csv('input_dataframe.csv')  

    else:
        print("\nIts a STOCK \n", symbol)


        #Stocks
        try:
            name = driver.find_element_by_xpath('//*[@id="quote-header-info"]/div[2]/div[1]/div[1]/h1').text
        except:
            name = "none"

        try:
            current = driver.find_element_by_xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/fin-streamer[1]').text
        except:
            current = 'none'

        try:
            change = driver.find_element_by_xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/fin-streamer[2]/span').text
        except:
            change = "none"

        try:
            change_percentage = driver.find_element_by_xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/fin-streamer[3]/span').text.replace('(','').replace(')','')
        except:
            change_percentage="none"

        try:
            previous_close = driver.find_element_by_xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[1]/td[2]').text
        except:
            previous_close = "none"

        try:
            Open = driver.find_element_by_xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[2]/td[2]').text
        except:
            Open = "none"

        try:
            day_range_min = driver.find_element_by_xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[5]/td[2]').text.split("-")[0]
        except:
            day_range_min = "none"

        try:
            day_range_max = driver.find_element_by_xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[5]/td[2]').text.split("-")[1]
        except:
            day_range_max = "none"

        try:
            _52_week_range_min = driver.find_element_by_xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[6]/td[2]').text.split("-")[0]
        except:
            _52_week_range_min = "none"

        try:
            _52_week_range_max = driver.find_element_by_xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[6]/td[2]').text.split("-")[1]
        except:
            _52_week_range_max = "none"

        try:
            volume = driver.find_element_by_xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[7]/td[2]').text
        except:
            volume = "none"

        try:
            average_volume = driver.find_element_by_xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[8]/td[2]').text
        except:
            average_volume = "none"

        try:
            market_cap = driver.find_element_by_xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[1]/td[2]').text
        except:
            market_cap = "none"

        try:
            beta = driver.find_element_by_xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[2]/td[2]').text
        except:
            beta = "none"

        try:
            pe_ratio = driver.find_element_by_xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[3]/td[2]').text
        except:
            pe_ratio = "none"

        try:
            eps = driver.find_element_by_xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[4]/td[2]').text
        except:
            eps = "none"

        try:
            forward_dividend = driver.find_element_by_xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[6]/td[2]').text.split(" ")[0]
        except:
            forward_dividend = "none"

        try:
            Yield = driver.find_element_by_xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[6]/td[2]').text.split(" ")[1].replace('(','').replace(')','')
        except:
            Yield = "none"

        timestamp = datetime.datetime.now()


        #making dictonary
        data = {
            'symbol':symbol,
            'name':name,
            'current':current.replace(",",""),
            'change':change,
            'change_percentage': change_percentage,
            'previous_close':previous_close.replace(",",""),
            'open':Open.replace(",",""),
            'volume':volume.replace(",",""),
            'day_range_min':day_range_min.replace(",",""),
            'day_range_max': day_range_max.replace(",",""),
            '52_week_range_min':_52_week_range_min.replace(",",""),
            '52_week_range_max': _52_week_range_max.replace(",",""),
            'avg_volume': avg_volume.replace(",",""),
            'market_cap':market_cap,
            'beta':beta,
            'pe_ratio':pe_ratio,
            'eps':eps,
            'forward_dividend':forward_dividend,
            'yield':Yield,
            'timestamp':str(timestamp)
         }


        #append it to main data
        main.append(data)
        print("Making JSON")
        #Open and save in json file
        with open("demo.json", 'w', encoding="utf-8") as f:
                  json.dump(main, f,indent=4, ensure_ascii=False)


        #creating dataframe
        df = df.append({
            'symbol':symbol,
            'name':name,
            'current':current.replace(",",""),
            'change':change,
            'change_percentage': change_percentage,
            'previous_close':previous_close.replace(",",""),
            'open':Open.replace(",",""),
            'volume':volume.replace(",",""),
            'day_range_min':day_range_min.replace(",",""),
            'day_range_max': day_range_max.replace(",",""),
            '52_week_range_min':_52_week_range_min.replace(",",""),
            '52_week_range_max': _52_week_range_max.replace(",",""),
            'avg_volume': avg_volume.replace(",",""),
            'market_cap':market_cap,
            'beta':beta,
            'pe_ratio':pe_ratio,
            'eps':eps,
            'forward_dividend':forward_dividend,
            'yield':Yield,
            'timestamp':str(timestamp)
         }, ignore_index=True)

        print("Making csv")
        df.to_csv('input_dataframe.csv')  
