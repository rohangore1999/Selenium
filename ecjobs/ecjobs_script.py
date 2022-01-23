import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import numpy as np
import json
import requests

import re
from collections import OrderedDict
from time import strptime

import sys


# list of dictionary
main = []

# Initializing data Frame
df = pd.DataFrame()

driver = webdriver.Chrome(executable_path=r"chromedriver.exe")
driver.get('https://www.ecjobsonline.com/search-results-jobs/?searchId=1639064028.6211&action=search&page=1&listings_per_page=20&view=list')


links = []

# pages
for pg in range(1, 2000000):
    print("\n GETTING ONLY LINKS from page no: >>>> \n", pg)
    if '◀' in driver.find_elements_by_class_name('pink_arrows')[-1].text:
        break
    else:
        #visitng each page
        driver.get(f'https://www.ecjobsonline.com/search-results-jobs/?searchId=1639064028.6211&action=search&page={pg}&listings_per_page=20&view=list')
        
        #getting each link from each page
        for ep in range(20):
            try:
                # getting links
                link = driver.find_element_by_class_name('job-list').find_elements_by_tag_name('tr')[ep].get_attribute('onclick').split('"')[1]
                print(link)
                links.append(link)
            except Exception as e:
                print(e)
                pass

print("\n ALL LINKS SCRAPED, NOW VISIT EACH LINKS >>>> \n")

# for each link from list
for el in range(len(links)):
    print("\n LINK >>>> \n", links[el])
    driver.get(links[el])
    
    # job title and company
    try:
        job_title_company = driver.find_element_by_xpath('//*[@id="listingsResults"]/div/div[3]/h2/span').text
    except:
        job_title_company='na'
        
    try:
        job_name = driver.find_element_by_xpath('//*[@id="listingsResults"]/div/div[3]/h3').text
    except:
        job_name ='na'
    
    try:
        company_pic_url = driver.find_element_by_xpath('//*[@id="listingsResults"]/div/img').get_attribute('src')
        response = requests.get(company_pic_url)
        
        try:
            fnme = job_title_company.split(" ")[0]
        except:
            fnme = job_title_company
            pass
        
        file = open(f"imgs/{fnme}'_'{driver.current_url.split('/')[4]}.png", "wb")
        file.write(response.content)
        file.close()
    except Exception as e:
        print(e)
        company_pic_url = 'na'
    
    try:
        secondary_name = driver.find_element_by_xpath('//*[@id="listingsResults"]/div/div[3]/span[1]/div[1]/h2').text
    except:
        secondary_name = 'na'

    try:
        jobdescription = driver.find_element_by_xpath('//*[@id="listingsResults"]/div/div[3]/span[2]').get_attribute('innerHTML')
    except:
        jobdescription = 'na'

    # job info
    try:
        job_info = driver.find_element_by_xpath('//*[@id="displayListing"]/div[3]/div[5]/div[2]').text.replace('\n',' ').split(": ")[-1]
    except:
        job_info = 'na'

    # email
    try:
        email = driver.find_element_by_xpath('//*[@id="displayListing"]/div[3]/div[7]/div[2]/span[2]').text
    except:
        email="na"

    #contact
    try:
        contact = driver.find_element_by_xpath('//*[@id="displayListing"]/div[3]/div[7]/div[2]/span[4]').text
    except:
        contact = 'na'
    

    # whatsapp
    try:
        whatsapp = driver.find_element_by_xpath('//*[@id="displayListing"]/div[3]/div[7]/div[2]/span[6]').text
    except:
        whatsapp = 'na'

    #website
    try:
        website = driver.find_element_by_xpath('//*[@id="displayListing"]/div[3]/div[7]/div[2]/span[8]').text
    except:
        website = 'na'

    # salary
    try:
        salary = driver.find_element_by_xpath('//*[@id="displayListing"]/div[3]/div[9]/div[2]/span[2]').text
    except:
        salary = 'na'

    #workinglocation
    try:
        workinglocation = driver.find_element_by_xpath('//*[@id="displayListing"]/div[3]/div[9]/div[2]/span[4]').text
    except:
        workinglocation = 'na'

    # jobfuncion
    try:
        jobfunction = driver.find_element_by_xpath('//*[@id="displayListing"]/div[3]/div[9]/div[2]/span[6]').text
    except:
        jobfunction = 'na'

    #industry
    try:
        industry = driver.find_element_by_xpath('//*[@id="displayListing"]/div[3]/div[9]/div[2]/span[8]').text
    except:
        industry = 'na'

    #employmentterm
    try:
        employmentterm = driver.find_element_by_xpath('//*[@id="displayListing"]/div[3]/div[9]/div[2]/span[10]').text
    except:
        employmentterm = 'na'


    # experience
    try:
        experience = driver.find_element_by_xpath('//*[@id="displayListing"]/div[3]/div[9]/div[2]/span[12]').text
    except:
        experience = 'na'


    # educationlevel
    try:
        educationlevel = driver.find_element_by_xpath('//*[@id="displayListing"]/div[3]/div[9]/div[2]/span[14]').text
    except:
        educationlevel = 'na'


    # careerlevel
    try:
        careerlevel = driver.find_element_by_xpath('//*[@id="displayListing"]/div[3]/div[9]/div[2]/span[16]').text
    except:
        careerlevel = 'na'


    # benefit
    try:
        benefit = driver.find_element_by_xpath('//*[@id="displayListing"]/div[3]/div[9]/div[2]/span[18]').text.replace('\n',', ')
    except:
        benefit = 'na'
    
    
    
    #making dictonary
    data = {
        'id':driver.current_url.split('/')[4],
        'job_post_url':driver.current_url,
        'company_pic_url':company_pic_url,
        'job_title_company':job_title_company,
        'first_name':secondary_name,
        'jobdescription': jobdescription,
        'job_info':job_info,
        'email':email,
        'whatsapp':whatsapp,
        'website':website,
        'salary': salary,
        'workinglocation':workinglocation,
        'employmentterm': employmentterm,
        'experience': experience,
        'educationlevel':educationlevel,
        'careerlevel':careerlevel,
        'benefit':benefit,
        'jobfunction':jobfunction,
        'industry':industry,
        'contact':contact,
        'jobfunction':jobfunction,
        'job_name':job_name
        
     }


    #append it to main data
    main.append(data)
    print("Making JSON")
    #Open and save in json file
    with open("demo.json", 'w', encoding="utf-8") as f:
              json.dump(main, f,indent=4, ensure_ascii=False)

    #creating dataframe
    df = df.append({
        'id':driver.current_url.split('/')[4],
        'job_post_url':driver.current_url,
        'company_pic_url':company_pic_url,
        'job_title_company':job_title_company,
        'first_name':secondary_name,
        'jobdescription': jobdescription,
        'job_info':job_info,
        'email':email,
        'whatsapp':whatsapp,
        'website':website,
        'salary': salary,
        'workinglocation':workinglocation,
        'employmentterm': employmentterm,
        'experience': experience,
        'educationlevel':educationlevel,
        'careerlevel':careerlevel,
        'benefit':benefit,
        'jobfunction':jobfunction,
        'industry':industry,
        'contact':contact,
        'jobfunction':jobfunction,
        'job_name':job_name
        
     }, ignore_index=True)

    print("Making csv")
    df.to_csv('input_dataframe.csv')    