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

# list of dictionary
main = []

# Initializing data Frame
df = pd.DataFrame()


driver = webdriver.Chrome(executable_path=r"chromedriver.exe")


driver.get("https://www.eaa.labour.gov.hk/en/result.html?page-no=1&row-per-page=30&list_all_agencies=all&sort-by=TC_NAME_ASC&types=")

# terms and conditions
sleep(1)
driver.find_element_by_xpath('//*[@id="button-i-accept"]').click()
sleep(1)
driver.find_element_by_xpath('//*[@id="button-i-accept"]').click()
    
# pg no(1 to 111)
for pg in range(1,112):
    print("\n****** Page "+str(pg)+" ongoing******\n")
    driver.get("https://www.eaa.labour.gov.hk/en/result.html?page-no="+str(pg)+"&row-per-page=30&list_all_agencies=all&sort-by=TC_NAME_ASC&types=")
    
    # companies(per pg 30)
    for c in range(0, 29):
        try:
            link = driver.find_elements_by_class_name('result')[c].find_element_by_class_name('right').find_element_by_tag_name('a').get_attribute('href')

            agency_id = link.split('&')[-1].split('=')[-1]
            
            driver.get(link)

            company_name = driver.find_element_by_class_name('main-content').find_element_by_tag_name('h2').text
            print(company_name)
            print(" ")
            if company_name == " ":
                company_name = "None"

            try:
                chinese_company_name = driver.find_element_by_class_name('main-content').find_element_by_class_name('chi-name').text
            except:
                chinese_company_name = "None"

            print(chinese_company_name)
            print(" ")
            if chinese_company_name == " ":
                chinese_company_name = "None"

            valid_license = driver.find_element_by_class_name('main-content').find_elements_by_tag_name('p')[1].text   
            if valid_license == " ":
                valid_license = "None"

            district = driver.find_element_by_class_name('main-content').find_elements_by_tag_name('p')[3].text
            if district == " ":
                district = "None"

                
            address = driver.find_element_by_class_name('main-content').find_elements_by_tag_name('p')[5].text  
            if address == " ":
                address = "None"

                
            telephone = driver.find_element_by_class_name('main-content').find_elements_by_tag_name('p')[7].text    
            if telephone == " ":
                telephone = "None"

                
            fax = driver.find_element_by_class_name('main-content').find_elements_by_tag_name('p')[9].text     
            if fax == " ":
                fax = "None"

                
            email = driver.find_element_by_class_name('main-content').find_elements_by_tag_name('p')[11].text    
            if email == " ":
                email = "None"

                
            placement_type = driver.find_element_by_class_name('main-content').find_elements_by_tag_name('p')[13].text     
            if placement_type == " ":
                placement_type = "None"

            # go back
            driver.back()

            # print("making dict")
            #making dictonary
            data ={
             'company_name': company_name,
             'chinese_company_name': chinese_company_name,
             'agency_id':agency_id,
             'valid_license':valid_license,
             'district':district,
             'address':address,
             'telephone':telephone,
             'fax': fax,
             'email':email,
             'placement_type': placement_type
             }
    #                     print(data)

            #append it to main data
            main.append(data)
            # print("Making JSON")
            #Open and save in json file
            with open("demo.json", 'w', encoding="utf-8") as f:
                      json.dump(main, f,indent=4, ensure_ascii=False)

            #creating dataframe
            df = df.append({
             'company_name': company_name,
             'chinese_company_name': chinese_company_name,
             'agency_id':agency_id,
             'valid_license':valid_license,
             'district':district,
             'address':address,
             'telephone':telephone,
             'fax': fax,
             'email':email,
             'placement_type': placement_type
             }, ignore_index=True)

            # print("Making csv")
            df.to_csv('demo.csv')
            
        except Exception as e:
            print(e)
