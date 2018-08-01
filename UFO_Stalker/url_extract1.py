# -*- coding: utf-8 -*-
import re
import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementNotVisibleException
)

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

url = 'http://www.ufostalker.com/tag/photo'


#initialising the chrome driver for selenium
def init_driver():
    driver = webdriver.Chrome('/Users/d3admin/Desktop/BigData/599ProjectWork/Assignment2/chromedriver')
    driver.wait = WebDriverWait(driver, 5)
    return driver
driver = init_driver()
driver.get(url)

#extracting the image urls from event id 20k-40k
f = open('urls_images1.txt', 'a',0)
for i in range(20000,40000):
    try:
        url = "http://www.ufostalker.com/event/"+str(i)
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.ID, 'event-detail-title'))) #wait until the event page has loaded
        matches = re.findall(r'(?:http\:|https\:)?\/\/www\.mufoncms\.com.*\.(?:png|jpg|jpeg)', driver.page_source, re.IGNORECASE) #regex to match the image urls 
        if len(matches) > 0:
            for match in matches:
                f.write(match+"\n")
                f.flush()
                os.fsync(f)
    except:
        print i







        
    