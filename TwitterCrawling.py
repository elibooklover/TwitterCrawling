#Script Name: TwitterCrawling.py
#Location: /Users/hoyeolkim/Box/GitHub/Python_Script/Programs/TwitterCrawling.py
#Created by Hoyeol Kim
#Creation Date: 05/25/2019
#Purpose: Twitter Crawling with Python
#Last Modified: 07/26/2019

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from selenium.webdriver.common.keys import Keys
import datetime as dt

# For Windows
#binary=FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')
#browser=webdriver.Firefox(firefox_binary=binary, executable_path='C:\Python37\geckodriver.exe')

# For macOS
binary=FirefoxBinary(r'/Applications/Firefox.app/Contents/MacOS/firefox')
# Change the path
browser=webdriver.Firefox(firefox_binary=binary, executable_path='/Users/hoyeolkim/Library/Python/3.7/bin/geckodriver')

startdate=dt.date(month=1,day=1,year=2019)
untildate=dt.date(month=1,day=2,year=2019)
enddate=dt.date(month=1,day=7,year=2019)

totalfreq=[]
while not enddate==startdate:
    # Search Keyword
    url='https://twitter.com/search?q=George Eliot%20since%3A'+str(startdate)+'%20until%3A'+str(untildate)+'&amp;amp;amp;amp;amp;amp;lang=eg'
    browser.get(url)
    html = browser.page_source
    soup=BeautifulSoup(html,'html.parser')
    
    lastHeight = browser.execute_script("return document.body.scrollHeight")
    while True:
            dailyfreq={'Date':startdate}
    # i=0 i is a page number
            wordfreq=0
            tweets=soup.find_all("p", {"class": "TweetTextSize"})
            wordfreq+=len(tweets)
                
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            
            newHeight = browser.execute_script("return document.body.scrollHeight")
            print(newHeight)
            if newHeight != lastHeight:
                html = browser.page_source
                soup=BeautifulSoup(html,'html.parser')
                tweets=soup.find_all("p", {"class": "TweetTextSize"})
                wordfreq=len(tweets)
            else:
                dailyfreq['Frequency']=wordfreq
                wordfreq=0
                totalfreq.append(dailyfreq)
                startdate=untildate
                untildate+=dt.timedelta(days=1)
                dailyfreq={}
                break
    #         i+=1
            lastHeight = newHeight

import pandas as pd
df=pd.DataFrame(totalfreq)
df.head()

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

import matplotlib.pyplot as plt
plt.figure(figsize=(20,10))
plt.xticks(rotation=90)
plt.rcParams["date.autoformatter.day"] = "%m/%d/%Y"
plt.scatter(df.Date,df.Frequency)
plt.show()
