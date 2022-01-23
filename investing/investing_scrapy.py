from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import json
from collections import OrderedDict
import pandas as pd


import time
from datetime import datetime
from datetime import date

# list of dictionary
main = []

# Initializing data Frame
df = pd.DataFrame()

# to get today's date
today = date.today()

print("Todays date is ==> ", today)

dt = datetime(today.year, today.month, today.day)
integer = int(round(dt.timestamp() * 1))

driver = webdriver.Chrome(executable_path=r"chromedriver.exe")

file = open("input_links.txt", "r")
links = file.read()

links = links.replace('\n',"").split(",")


for l in links:
    try:
        #link = f'https://in.investing.com/equities/3m-india-historical-data?end_date={integer}&st_date=1483641000'

        l = l+f'?end_date={integer}&st_date=1483641000'
        print('Link is =>', l)
        driver.get(l)

        len_data = len(driver.find_element_by_class_name('main-container').find_elements_by_class_name('common-table-item'))

        #Company Name
        company_name = driver.find_element_by_class_name('main-title-wrapper').find_element_by_class_name('main-title').text
        print("Company => ", company_name)
        for ld in range(len_data):
            try:
                #date
                date = driver.find_element_by_class_name('main-container').find_elements_by_class_name('common-table-item')[ld].find_element_by_class_name('col-rowDate').text

                #price
                price = driver.find_element_by_class_name('main-container').find_elements_by_class_name('common-table-item')[ld].find_element_by_class_name('col-last_close').text

                #Open
                Open = driver.find_element_by_class_name('main-container').find_elements_by_class_name('common-table-item')[ld].find_element_by_class_name('col-last_open').text

                #High
                High = driver.find_element_by_class_name('main-container').find_elements_by_class_name('common-table-item')[ld].find_element_by_class_name('col-last_max').text

                #low
                low = driver.find_element_by_class_name('main-container').find_elements_by_class_name('common-table-item')[ld].find_element_by_class_name('col-last_min').text

                #volume
                volume = driver.find_element_by_class_name('main-container').find_elements_by_class_name('common-table-item')[ld].find_element_by_class_name('col-volume').text

                #chg %
                chg_per = driver.find_element_by_class_name('main-container').find_elements_by_class_name('common-table-item')[ld].find_element_by_class_name('col-change_percent').text

                #making dictonary
                data = {
                    'company_name':company_name,
                    'date':date,
                    'price':price,
                    'Open': Open,
                    'High': High,
                    'low':low,
                    'volume':volume,
                    'chg_per':chg_per
                 }


                #append it to main data
                main.append(data)
                print("Making JSON")
                #Open and save in json file
                with open("demo.json", 'w', encoding="utf-8") as f:
                          json.dump(main, f,indent=4, ensure_ascii=False)  

                #creating dataframe
                df = df.append({
                    'Company Name':company_name,
                    'date':date,
                    'price':price,
                    'Open': Open,
                    'High': High,
                    'low':low,
                    'volume':volume,
                    'chg_per':chg_per
                 }, ignore_index=True)

                print("Making csv")
                df.to_csv('input_dataframe.csv',columns=["Company Name","date","price","Open","High","low","volume","chg_per"])

            except Exception as e:
                print(e)
                
    except Exception as e:
            print(e)