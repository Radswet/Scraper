from math import prod
from bs4 import BeautifulSoup
import pymongo
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
load_dotenv()


CONNECTION_STRING = os.getenv('CONNECTION_STRING')

client = pymongo.MongoClient(CONNECTION_STRING)
mydb = client["Cluster0"]
mycol = mydb["Falabella"]

website = 'https://www.falabella.com/falabella-cl/category/cat690299/Figuras-de-accion-y-coleccionables?page={}'

page = 1



options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
chromedriver_path = "./chromedriver_linux64/chromedriver"
driver = webdriver.Chrome(chromedriver_path)

#driver.quit()





while True:
    try:
        url = website.format(page) 
        driver.get(url)
        time.sleep(3)
        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')
        
        product = soup.findAll('div',class_="jsx-3128226947")
        
        for p in product:
            url=p.find('a')['href']
            data = {"url":url}
            mycol.insert_one(data)

        page+=1
        
        
    except:
        break
        print("404")
    