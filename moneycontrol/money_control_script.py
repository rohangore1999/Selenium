import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import json


import re
from collections import OrderedDict
from time import strptime

import sys

import time
from datetime import datetime
from datetime import date

import warnings
warnings.filterwarnings('ignore')

today = date.today()
today_date = today.strftime("%d-%b-%Y")

# list of dictionary
main = []

try:
    df = pd.read_csv('input_dataframe.csv')
    df.drop('Unnamed: 0', axis=1, inplace=True)
except:
    # Initializing data Frame
    df = pd.DataFrame()

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(chrome_options=options,executable_path=r"chromedriver.exe")


input_link = str(input("Please paste link here... "))
driver.get(input_link)

driver.execute_script("window.scrollBy(0,925)", "")

sleep(20)
# click on types => all indices
driver.find_element_by_id('indicesDropdown').find_elements_by_tag_name('option')[-1].click()

sleep(5)
#to get length of the nse links
nse_links_len = len(driver.find_element_by_class_name('ntlist').find_elements_by_class_name('indicesList'))

nse_links = []
nse_names = []

sleep(5)
for nl in range(nse_links_len):
    #to get links
    nl_link = driver.find_element_by_class_name('ntlist').find_elements_by_class_name('indicesList')[nl].find_element_by_tag_name('a').get_attribute('href')
    nse_links.append(nl_link)
    
    # name
    nse_name = driver.find_element_by_class_name('ntlist').find_elements_by_class_name('indicesList')[nl].text
    nse_names.append(nse_name)

#getting data
for nse_link,nse_name in zip(nse_links,nse_names):
    try:
        print("NSE TYPE => ", nse_name)
        driver.get(nse_link)
        sleep(5)
        
        #length of stocks list
        stocklist_len = len(driver.find_element_by_id('tableslider').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr'))    
        
        # 0-9 for every col
        for d in range(stocklist_len):
            try:
                name = driver.find_element_by_id('tableslider').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[d].find_elements_by_tag_name('td')[0].text
                ltp = driver.find_element_by_id('tableslider').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[d].find_elements_by_tag_name('td')[1].text
                change = driver.find_element_by_id('tableslider').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[d].find_elements_by_tag_name('td')[2].text
                volume = driver.find_element_by_id('tableslider').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[d].find_elements_by_tag_name('td')[3].text
                buy_price = driver.find_element_by_id('tableslider').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[d].find_elements_by_tag_name('td')[4].text
                sell_price = driver.find_element_by_id('tableslider').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[d].find_elements_by_tag_name('td')[5].text
                buy_qty = driver.find_element_by_id('tableslider').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[d].find_elements_by_tag_name('td')[6].text
                sell_qty = driver.find_element_by_id('tableslider').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[d].find_elements_by_tag_name('td')[7].text
                Open = driver.find_element_by_id('tableslider').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[d].find_elements_by_tag_name('td')[8].text
                prev_close = driver.find_element_by_id('tableslider').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[d].find_elements_by_tag_name('td')[9].text


                #making dictonary
                data ={
                    'date': today_date,
                    'nse_type': nse_name,
                    'name':name,
                    'ltp':ltp,
                    'change': change,
                    'volume':volume,
                    'buy_price':buy_price,
                    'sell_price':sell_price,
                    'buy_qty':buy_qty,
                    'sell_qty': sell_qty,
                    'Open': Open,
                    'Prev Close':prev_close
                 }


                #append it to main data
                main.append(data)
                print("Making JSON")
                #Open and save in json file
                with open("demo.json", 'w', encoding="utf-8") as f:
                          json.dump(main, f,indent=4, ensure_ascii=False)

                #creating dataframe
                df = df.append({
                    'date': today_date,
                    'nse_type': nse_name,
                    'name':name,
                    'ltp':ltp,
                    'change': change,
                    'volume':volume,
                    'buy_price':buy_price,
                    'sell_price':sell_price,
                    'buy_qty':buy_qty,
                    'sell_qty': sell_qty,
                    'Open': Open,
                    'Prev Close':prev_close
                 }, ignore_index=True)

                print("Making csv")
                df.to_csv('input_dataframe.csv',columns=["date",'nse_type',"name","ltp","change","volume","buy_price","sell_price","buy_qty","sell_qty", "Open", "Prev Close"])
            except Exception as e:
                print(e)
    except Exception as e:
                print(e)