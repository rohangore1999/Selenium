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


# Capital 1st letter after space
def cap_each(string):
    list_of_words = string.split(" ")

    for word in list_of_words:
        list_of_words[list_of_words.index(word)] = word.capitalize()

    return " ".join(list_of_words)


driver = webdriver.Chrome(executable_path=r"chromedriver.exe")
# driver.get("https://appdevelopmentcompanies.co/local-agencies/in/app-developers/indore")
file = open("input_links.txt", "r")
links = file.read()
links = links.replace('\n',"").split(",")

for link in links:
    try:
        print("Link => ",link)
        driver.get(link)
        
        com_len = len(driver.find_element_by_class_name('company-listing').find_elements_by_class_name('list-item'))

        #title
        title = driver.find_element_by_class_name('company-details').text.split("|")[0]

        #location
        if 'in' in title:
            location = driver.find_element_by_class_name('company-details').text.split("|")[0].split('in')[1]
        else:
            location = driver.find_element_by_class_name('company-details').text.split("|")[0].split('In')[1]

        for c in range(com_len):
            try:
                # companyname
                try:
                    companyname = driver.find_element_by_class_name('company-listing').find_elements_by_class_name('list-item')[c].find_element_by_tag_name('h3').text.split(" ")[1]
                    print("Company Name => ", companyname)
                except:
                    companyname = "na"

                # companylogo
                try:
                    companylogo = driver.find_element_by_class_name('company-listing').find_elements_by_class_name('list-item')[c].find_element_by_class_name('image').find_element_by_tag_name('img').get_attribute('src')
                except:
                    companylogo = "na"

                # websitelink
                try:
                    websitelink = driver.find_element_by_class_name('company-listing').find_elements_by_class_name('list-item')[c].find_element_by_tag_name('h3').find_element_by_tag_name('a').get_attribute('href')
                except:
                    websitelink = 'na'

                # founded
                try:
                    founded = driver.find_element_by_class_name('company-listing').find_elements_by_class_name('list-item')[c].find_element_by_class_name('details').find_element_by_class_name('feature-list').find_elements_by_tag_name('tr')[0].text.split(":")[1]
                except:
                    founded = 'na'

                # horulyrate
                try:
                    horulyrate = driver.find_element_by_class_name('company-listing').find_elements_by_class_name('list-item')[c].find_element_by_class_name('details').find_element_by_class_name('feature-list').find_elements_by_tag_name('tr')[1].text.split(":")[1]
                except:
                    horulyrate = 'na'

                # employee
                try:
                    employee = driver.find_element_by_class_name('company-listing').find_elements_by_class_name('list-item')[c].find_element_by_class_name('details').find_elements_by_class_name('feature-list')[0].find_elements_by_tag_name('tr')[2].text.split(":")[1]
                except:
                    employee = 'na'

                # contact
                try:
                    contact = driver.find_element_by_class_name('company-listing').find_elements_by_class_name('list-item')[c].find_element_by_class_name('details').find_elements_by_class_name('feature-list')[1].find_elements_by_tag_name('tr')[0].text.split(":")[1]
                except:
                    contact = 'na'

                # email
                try:
                    email = driver.find_element_by_class_name('company-listing').find_elements_by_class_name('list-item')[c].find_element_by_class_name('details').find_elements_by_class_name('feature-list')[1].find_elements_by_tag_name('tr')[1].text.split(":")[1]
                except:
                    email = 'na'

                # clutchrating
                try:
                    clutchrating = driver.find_element_by_class_name('company-listing').find_elements_by_class_name('list-item')[c].find_element_by_class_name('details').find_elements_by_class_name('feature-list')[1].find_elements_by_tag_name('tr')[2].text.split(":")[1]
                except:
                    clutchrating = 'na'

                # servicelength
                try:
                    ser_len = len(driver.find_element_by_class_name('company-listing').find_elements_by_class_name('list-item')[c].find_element_by_class_name('details').find_element_by_class_name('service-line').find_elements_by_class_name('owl-item'))

                    services = []
                    for s in range(ser_len):
                        service = driver.find_element_by_class_name('company-listing').find_elements_by_class_name('list-item')[c].find_element_by_class_name('details').find_element_by_class_name('service-line').find_elements_by_class_name('owl-item')[s].find_element_by_tag_name('img').get_attribute('alt')
                        service = service.replace('-',' ')
                        service = cap_each(service)
                        services.append(service)
                        
                    services = ','.join(services)
                except:
                    serveces = 'na'

                #making dictonary
                data ={
                    'title':title,
                    'location':location,
                    'companyname': companyname,
                    'companylogo':companylogo,
                    'websitelink':websitelink,
                    'founded':founded,
                    'employee':employee,
                    'contact': contact,
                    'email':email,
                    'clutchrating': clutchrating,
                    'services': services
                 }


                #append it to main data
                main.append(data)
                print("Making JSON")
                #Open and save in json file
                with open("company_details.json", 'w', encoding="utf-8") as f:
                          json.dump(main, f,indent=4, ensure_ascii=False)

                #creating dataframe
                df = df.append({
                    'title':title,
                    'location':location,
                    'companyname': companyname,
                    'companylogo':companylogo,
                    'websitelink':websitelink,
                    'founded':founded,
                    'employee':employee,
                    'contact': contact,
                    'email':email,
                    'clutchrating': clutchrating,
                    'services': services
                 }, ignore_index=True)

                print("Making csv")
                df.to_csv('company_details.csv')

                print(" ")

            except:
                pass
        
    except Exception as e:
        print(e)