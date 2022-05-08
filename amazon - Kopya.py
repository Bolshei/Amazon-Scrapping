from bs4 import BeautifulSoup
import requests
import csv
from selenium.webdriver.chrome.service import Service
from selenium import webdriver



def get_url(search_term):
    template="https://www.amazon.com.tr/s?k={}"
    search_term=search_term.replace(' ', '+')
    url=template.format(search_term)
    url+='&page={}'
    return url


def extract_record(item):

    #description and url
    atag=item.h2.a
    description=atag.text.strip()
    url='https://www.amazon.com.tr' + atag.get('href')

    try:
        #price
        price_parent=item.find('span', 'a-price')
        price=price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        return

    try:
        #rank and rating
        rating= item.i.text
        review_count=item.find('span', {'class': 'a-size-base s-underline-text'}).text
    except AttributeError:
        rating = ''
        review_count=''

    result= (description,price,rating,review_count,url)
    return result

def main(search_term):
    s = Service('C:\\chromedriver.exe')
    driver = webdriver.Chrome(service=s)

    records=[]
    url= get_url(search_term)
    for page in range(1,10):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        for item in results:
            record= extract_record(item)
            if record:
                records.append(record)
    driver.close()
    with open('results.csv','w',newline='',encoding='utf-8') as f:
        writer=csv.writer(f,delimiter = '|')
        writer.writerow(['Description','Price','Rating','ReviewCount','Url'])
        writer.writerows(records)

main('ps4')


