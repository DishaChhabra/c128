from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests

url = 'https://exoplanets.nasa.gov/discovery/exoplanet-catalog/'

#webdriver.Edge
browser = webdriver.Chrome('./chromedriver.exe')
browser.get(url)
time.sleep(10)
headers = ['NAME',	'LIGHT-YEARS FROM EARTH',	'PLANET MASS',	'STELLAR MAGNITUDE',   'DISCOVERY DATE', 'HYPERLINK', 'PLANET TYPE', 'PLANET RADIUS','ORBITAL RADIUS', 'ORBITAL PERIOD', 'ECCENTRICITY']
data = []
def get_data():
    for i in range(0,5):
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        for a in soup.find_all('ul', attrs={'class','exoplanet'}):
            li = a.find_all('li')
            temp = []
            for w,o in enumerate(li):
                if w == 0:
                    temp.append(o.find_all('a')[0].contents[0])
                else:
                    try: 
                        temp.append(o.contents[0])
                    except:
                        temp.append("")
            tag = li[0]
            temp.append('https://exoplanets.nasa.gov' + tag.find_all('a', href=True)[0]['href'])
            data.append(temp)
        browser.find_element('xpath','//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()
     

get_data()

newdata=[]
def getdata2(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    temp = []
    for i in soup.find_all('tr', attrs={'class': "fact_row"}):
        td = i.find_all('td')
        for o in td:
            temp.append(o.find_all('div', attrs={'class': 'value'})[0].contents[0])
        newdata.append(temp)

for a,p in enumerate(data):
    getdata2(p[5])

# print(newdata[0:5])

finaldata = []
for r,k in enumerate(data):
    # r = rownumber
    element = newdata[r]
    element = [i.replace('\n', '') for i in element ]
    element = element[:6]
    finaldata.append(k+element)

with open('dataaa.csv', 'w') as file:
        Writer = csv.writer(file)
        Writer.writerow(headers)
        Writer.writerows(finaldata) 

