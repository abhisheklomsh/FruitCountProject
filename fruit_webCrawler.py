#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
import re
import sys
import os
import http.cookiejar
import json
import urllib.request, urllib.error, urllib.parse
from selenium import webdriver
from bs4 import BeautifulSoup as soup
import time
import os
def get_soup(url,header):
    #return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),
    # 'html.parser')
    return BeautifulSoup(urllib.request.urlopen(
        urllib.request.Request(url,headers=header)),
        'html.parser')
#from selenium import webdriver
QueryList=["orange tree","Apple Tree"]
for query in QueryList:
    query = query.split()
    query = '+'.join(query)
    url="http://www.bing.com/images/search?q=" + query + "&FORM=HDRSC2"
    #driver=webdriver.Chrome()
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #add the directory for your image here
    DIR="Pict"+query
    #header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    #soup = get_soup(url,header)

    ActualImages=[]# contains the link for Large original images, type of  image

    driver = webdriver.Chrome()
    driver.get(url)
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      time.sleep(0.5)
      new_height = driver.execute_script("return document.body.scrollHeight")
      if new_height == last_height:
         break
      last_height = new_height
    time.sleep(10)
    from selenium.webdriver.common.keys import Keys
    try:
        elem = driver.find_element_by_class_name("btn_seemore")
        elem.send_keys(Keys.TAB)
        elem.click()
    except:
        pass


    while True:
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      time.sleep(0.5)
      new_height = driver.execute_script("return document.body.scrollHeight")
      if new_height == last_height:
         break
      last_height = new_height
    time.sleep(20)
    try:
        elem = driver.find_element_by_class_name("btn_seemore")
        elem.send_keys(Keys.TAB)
        elem.click()
    except:
        pass
    while True:
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      time.sleep(0.5)
      new_height = driver.execute_script("return document.body.scrollHeight")
      if new_height == last_height:
         break
      last_height = new_height
    time.sleep(20)


    for a in soup(driver.page_source, 'html.parser').find_all("a",{"class":"iusc"}):
        #print a
        mad = json.loads(a["m"])
        turl = mad["turl"]
        m = json.loads(a["m"])
        murl = m["murl"]

        image_name = urllib.parse.urlsplit(murl).path.split("/")[-1]
        print(image_name)

        ActualImages.append((image_name, turl, murl))

    print("there are total" , len(ActualImages),"images")

    if not os.path.exists(DIR):
        os.mkdir(DIR)

    DIR = os.path.join(DIR, query.split()[0])
    if not os.path.exists(DIR):
        os.mkdir(DIR)

    ##print images
    for i, (image_name, turl, murl) in enumerate(ActualImages):
        try:
            #req = urllib2.Request(turl, headers={'User-Agent' : header})
            #raw_img = urllib2.urlopen(req).read()
            #req = urllib.request.Request(turl, headers={'User-Agent' : header})
            raw_img = urllib.request.urlopen(turl).read()

            cntr = len([i for i in os.listdir(DIR) if image_name in i]) + 1
            #print cntr

            f = open(os.path.join(DIR, image_name), 'wb')
            f.write(raw_img)
            f.close()
        except Exception as e:
            print("could not load : " + image_name)
            print(e)



