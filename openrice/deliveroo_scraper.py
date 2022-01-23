import time
from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException
import json
import sys
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz

main = []


#Print Arguments
print("Passed Arguments are: "+str(sys.argv[1]))

f = str(sys.argv[1])

lan = f.split('_')[-1].split('.')[0]

driver = webdriver.Chrome(executable_path=r"chromedriver.exe")
driver.maximize_window()


with open(str(sys.argv[1]), encoding="utf8") as f:
    json_data = json.load(f)

for each_data in range(len(json_data)):
    for ordr in range(len(json_data[each_data]['order'])):
        try:
            if 'deliveroo.hk' in json_data[each_data]['order'][ordr]:

                ue_link = json_data[each_data]['order'][ordr]
                
                print("deliveroo link:", ue_link)

                if 'en' in sys.argv[1]:
                    if '/en/' in ue_link:
                        try:
                            # toggle language to english
                            ue_link = ue_link.replace('/zh/', '/en/')
                        except:
                            pass
                    else:
                        try:
                            # toggle language to english
                            ue_link = ue_link.replace("deliveroo.hk","deliveroo.hk/en")
                        except:
                            pass

                if 'zh' in sys.argv[1]:
                    if '/zh/' in ue_link:
                        try:
                            # toggle language to hk
                            ue_link = ue_link.replace('/en/', '/zh/')
                        except:
                            pass
                    else:
                        try:
                            # toggle language to english
                            ue_link = ue_link.replace("deliveroo.hk","deliveroo.hk/zh")
                        except:
                            pass

                driver.get(ue_link)
                
                try:
                    sleep(0.5)
                    driver.find_element_by_class_name("ccl-022adec8b2f34033").click()
                except:
                    pass

                try:
                    sleep(0.5)
                    driver.find_element_by_class_name("ccl-022adec8b2f34033").click()
                except:
                    pass
                
                try:
                    sleep(0.5)
                    driver.find_element_by_class_name("ccl-caaf537be0dac3d8").click()
                except:
                    pass

                try:
                    sleep(0.5)
                    driver.find_element_by_class_name("ccl-caaf537be0dac3d8").click()
                except:
                    pass

                try:
                    restaurant_name = driver.find_element_by_class_name("restaurant__details").find_element_by_tag_name('h1').text
                except:
                    restaurant_name = 'none'
                    
                try:    
                    rating = driver.find_element_by_class_name("orderweb__61671603").text.replace(')','').split('(')[0]
                except:
                    rating = 'none'

                try:
                    total_rating = driver.find_element_by_class_name("orderweb__61671603").text.replace(')','').split('(')[1].split(" ")[0]
                except:
                    total_rating = 'none'

                try:
                    cusine = driver.find_element_by_class_name("orderweb__8227a377").text.split("\n")[:-3]
                except:
                    cusine = 'none'

                try:
                    address = driver.find_element_by_class_name("orderweb__8227a377").text.split("\n")[-2]
                except:
                    address = "none"

                categories = []
                dish_names = []
                dish_prices = []
                dish_urls = []

                total_categories = len(driver.find_elements_by_class_name("orderweb__47414d10"))

                for _ in np.arange(1,10,0.1):
                    driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight/{_});")
                    sleep(0.1)


                for tc in range(total_categories):
                    categories.append(driver.find_elements_by_class_name("orderweb__47414d10")[tc].find_element_by_tag_name('h3').text)
                    
                    len_dish_name = len(driver.find_elements_by_class_name("orderweb__47414d10")[tc].find_element_by_class_name('orderweb__b75f90f9').find_elements_by_class_name('orderweb__0eecc2d3'))
                    
                    dish_name = []
                    dish_price = []
                    dish_url = []
                    
                    for dn in range(len_dish_name):
                        try:
                            dish_name.append(driver.find_elements_by_class_name("orderweb__47414d10")[tc].find_element_by_class_name('orderweb__b75f90f9').find_elements_by_class_name('orderweb__0eecc2d3')[dn].find_element_by_tag_name('p').text)
                        except:
                            dish_name.append('none')
                        
                        try:
                            dish_price.append(driver.find_elements_by_class_name("orderweb__47414d10")[tc].find_element_by_class_name('orderweb__b75f90f9').find_elements_by_class_name('orderweb__0eecc2d3')[dn].find_element_by_class_name('orderweb__19b2cfab').find_element_by_tag_name('span').text.replace('$',''))
                        except:
                            dish_price.append('none')
                            
                        try:
                            dish_url.append(driver.find_elements_by_class_name("orderweb__47414d10")[tc].find_element_by_class_name('orderweb__b75f90f9').find_elements_by_class_name('orderweb__0eecc2d3')[dn].find_element_by_class_name("orderweb__2cc612e1").find_element_by_class_name('ccl-45bd106b75353ec9').get_attribute('style').split('(')[1].split(')')[0].replace('"','').split('?')[0])
                        except:
                            dish_url.append('none')
                        
                    dish_names.append(dish_name)
                    dish_prices.append(dish_price)
                    dish_urls.append(dish_url)

                print("making dict")
                #making dictonary
                data = {
                 'url': driver.current_url,
                 'restaurant_name': restaurant_name,
                 'rating':rating,
                 'total_rating':total_rating,
                 'cusine':cusine,
                 'categories':categories,
                 'dish_names':dish_names,
                 'dish_prices':dish_prices,
                 'dish_urls':dish_urls,
                 'address':address,
                 'language': lan,
                 'unique_id': json_data[each_data]['unique_id']
                 }

                district = json_data[each_data]['district']
                language = json_data[each_data]['language']
                
                #append it to main data
                main.append(data)
                print("Making JSON")
                #Open and save in json file
                with open(f"deliveroo_{district}_{lan}.json", 'w', encoding="utf-8") as f:
                          json.dump(main, f,indent=4, ensure_ascii=False)
        except:
            pass