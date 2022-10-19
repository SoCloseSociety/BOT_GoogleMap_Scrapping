from calendar import c
from itertools import count
from operator import le
from xml.dom.minidom import Document
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import random
import socket


from selenium.common.exceptions import (
    ElementNotVisibleException,
    ElementClickInterceptedException,
    WebDriverException,
    TimeoutException,
)
import pyautogui
import pyperclip
import csv
import pandas as pd
from glob import glob
import os 
import random
from selenium.webdriver.common.keys import Keys

pyautogui.FAILSAFE = False

file_name = input("Filename : ")
search_query_link = input("Enter Link: ")

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

def is_connected():
  hostname = "one.one.one.one"  
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(hostname)
    # connect to the host -- tells us if the host is actually reachable
    s = socket.create_connection((host, 80), 2)
    s.close()
    return True
  except Exception:
     pass # we ignore any errors, returning False
  return False

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)  # version_main allows to specify your chrome version instead of following chrome global version
driver.maximize_window()

############################################################################################################
links = []

prev_links_length = 0
now_links_length = 0

count = 0

driver.get(search_query_link)  
time.sleep(10)
pyautogui.moveTo(100, 200)

while(True):
    count = count + 1
    html = driver.page_source
    soup = BeautifulSoup(html, features="html.parser")

    for a in soup.find_all('a', href=True):
        if '/maps/place/' in a['href']:
            links.append(a['href'])
    
    links = list(set(links))



    now_links_length = len(links)

    print(prev_links_length)
    print(now_links_length)

    if now_links_length == prev_links_length:
        if count % 50 == 0 :
            break
    else:
        prev_links_length = now_links_length

    pyautogui.scroll(-1000000)
    time.sleep(1)

print(len(links))

df = pd.DataFrame({"map_Link" : links})       
df.to_csv(file_name+"_map_links.csv", index=False)

driver.quit()
# #############################################################################################################
# #############################################################################################################
# #############################################################################################################
# #############################################################################################################

my_name= []
my_address= []
my_open_timing = []
my_website = []
my_phone_number = []

# file_name = 'm6'

with open(file_name+'_map_links.csv', 'r', encoding="utf-8") as file:
    reader = csv.reader(file)
    for row in reader:
        if '/' in row[0] and 'reserve/v/dine' not in row[0]:

            print(row[0])

            found_timing = False
            found_address = False
            found_website = False
            found_phone_number = False


            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)  # version_main allows to specify your chrome version instead of following chrome global version
            driver.maximize_window()
            driver.get(row[0]+"&hl=en")
            time.sleep(5)

            while(True):
                time.sleep(5)
                try:
                    driver.find_element(By.ID, 'searchbox')
                    break
                except:
                    driver.close()
                    os.system('nordvpn -c -g "United States"')
                    time.sleep(10)

                    while(True):
                        if(is_connected()==False):
                            os.system('nordvpn -c -g "United States"')
                            time.sleep(10)
                        elif(is_connected()==True):
                            break    

                    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options) 
                    driver.maximize_window()
                    driver.get(row[0]) 
            
            html = driver.page_source
            soup = BeautifulSoup(html, features="html.parser")

            name = soup.find('h1')
            name = name.text
            name = name.strip()
            print(name)
            my_name.append(name)

            div_aria_label = soup.findAll('div', attrs={"aria-label": True})

            for d in div_aria_label:
                if 'Information for' in d['aria-label']:
                    try:
                        mydivs_address = d.find_all("button", attrs={"data-item-id": "address"})
                        if(len(mydivs_address)>0):
                            for  i  in  mydivs_address:
                                address = i.text
                                address = address.strip()
                                if(len(address)>0):
                                    found_address = True
                                    my_address.append(address.strip())

                    except:
                        print("Address not found")

                    try:
                        mydivs_website = d.find_all("a", attrs={"data-item-id": "authority"})
                        if(len(mydivs_website)>0):
                            for  i  in  mydivs_website:
                                web = i['href']
                                if(len(web)>0):
                                    found_website = True
                                    my_website.append(web)
                    except:
                        print("Website not found")

                    try:
                        mydivs_phone = d.find_all("button", attrs={"aria-label": True})
                        if(len(mydivs_phone)>0):
                            for  i  in  mydivs_phone:
                                if 'Phone' in i['aria-label']:
                                    phn = i.text
                                    if(len(phn)>0):
                                        found_phone_number = True
                                        my_phone_number.append(i.text)     
                    except:
                        print("Phone number not found")


                elif 'Hide opening hours' in d['aria-label']:
                    found_timing = True
                    timing = d['aria-label']
                    timing = timing.split('.')
                    print(timing)
                    if len(timing[0])>0:
                        my_time = timing[0]
                        my_time = my_time.replace(","," -> ")

                        print(type(my_time))
                        my_open_timing.append(my_time)
                    else:
                        my_open_timing.append("None")

            if(found_timing == False):
                my_open_timing.append("None")
            if(found_address == False):
                my_address.append("None")
            if(found_website == False):
                my_website.append("None")
            if(found_phone_number == False):
                my_phone_number.append("None")



            print(len(my_name))
            print(len(my_address))
            print(len(my_open_timing))
            print(len(my_website))
            print(len(my_phone_number))
            


            time.sleep(2)

            dict = {'Name': my_name, 'Address': my_address, 'Opening schedule': my_open_timing, 'Wesite': my_website, 'Phone':my_phone_number} 
            df2 = pd.DataFrame(dict)

            df2.to_csv(file_name+'_map_details.csv') 

            driver.quit()
