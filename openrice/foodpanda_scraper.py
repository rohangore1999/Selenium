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
            if 'www.foodpanda.hk' in json_data[each_data]['order'][ordr]:

                fp_link = json_data[each_data]['order'][ordr]
                
                print("Food Panda link:", fp_link)
                driver.get(fp_link)
                sleep(0.5)
                driver.find_element_by_class_name('p-absolute').click()

                if 'en' in sys.argv[1]:
                    # toggle language
                    driver.find_element_by_xpath('//*[@id="global-header"]/header/div[2]/div/a[1]').click()

                if 'zh' in sys.argv[1]:
                    # toggle language
                    driver.find_element_by_xpath('//*[@id="global-header"]/header/div[2]/div/a[2]').click()
                try:
                    sleep(0.5)
                    driver.find_element_by_class_name('p-absolute').click()
                except:
                    pass



                try:
                    name = driver.find_element_by_class_name('vendor-info-main-details').text
                except:
                    name = 'none'

                try:
                    rating = driver.find_element_by_class_name('rating-label').text
                except:
                    rating = 'none'

                try:
                    len_cusine = len(driver.find_element_by_class_name('vendor-info-main-details-cuisines').find_elements_by_tag_name('li'))

                    cusines = []
                    for cs in range(len_cusine):
                        cusines.append(driver.find_element_by_class_name('vendor-info-main-details-cuisines').find_elements_by_tag_name('li')[cs].text)
                    cusines.pop(0)
                except:
                    cusines = "none"

                # scroll
                for _ in np.arange(1,10,0.1):
                    driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight/{_});")
                    sleep(0.1)

                try:
                    total_category = len(driver.find_element_by_class_name('menu__items-wrapper').find_elements_by_class_name('dish-category-section'))

                    category = []
                    dish_names = []
                    dish_prices = []
                    dsh_urls = []

                    for tc in range(total_category):
                        category.append(driver.find_element_by_class_name('menu__items-wrapper').find_elements_by_class_name('dish-category-section')[tc].find_element_by_class_name('dish-category-title').text)

                        dish_len = len(driver.find_element_by_class_name('menu__items-wrapper').find_elements_by_class_name('dish-category-section')[tc].find_element_by_class_name('dish-list').find_elements_by_class_name('dish-card'))

                        dish_name = []
                        dish_price = []
                        dsh_url = []

                        for dish in range(dish_len):
                            try:
                                dish_name.append(driver.find_element_by_class_name('menu__items-wrapper').find_elements_by_class_name('dish-category-section')[tc].find_element_by_class_name('dish-list').find_elements_by_class_name('dish-card')[dish].text.split("\n")[0])
                            except:
                                dish_name.append('none')

                            try:
                                dish_price.append(driver.find_element_by_class_name('menu__items-wrapper').find_elements_by_class_name('dish-category-section')[tc].find_element_by_class_name('dish-list').find_elements_by_class_name('dish-card')[dish].find_element_by_class_name('price').text.split('$ ')[1])
                            except:
                                dish_price.append('none')

                            try:
                                dsh_url.append(driver.find_element_by_class_name('menu__items-wrapper').find_elements_by_class_name('dish-category-section')[tc].find_element_by_class_name('dish-list').find_elements_by_class_name('dish-card')[dish].find_element_by_tag_name('picture').find_element_by_class_name('photo').get_attribute('style').split('(')[1].split(')')[0].replace('"','').split("?")[0])
                            except:
                                dsh_url.append('none')

                        dish_names.append(dish_name)
                        dish_prices.append(dish_price)
                        dsh_urls.append(dsh_url)
                except:
                    pass

                print("making dict")
                #making dictonary
                data = {
                 'url': driver.current_url,
                 'name': name,
                 'rating':rating,
                 'cusines':cusines,
                 'category':category,
                 'dish_name':dish_names,
                 'dish_price':dish_prices,
                 'dsh_url':dsh_urls,
                 'address':json_data[each_data]['address'],
                 'language': lan,
                 'unique_id': json_data[each_data]['unique_id']
                 }

                district = json_data[each_data]['district']
                language = json_data[each_data]['language']

                #append it to main data
                main.append(data)
                print("Making JSON")
                #Open and save in json file
                with open(f"foodpanda_{district}_{lan}.json", 'w', encoding="utf-8") as f:
                          json.dump(main, f,indent=4, ensure_ascii=False)
                
            break

        except:
            pass