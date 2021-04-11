import requests
from bs4 import BeautifulSoup
import time
import urllib.parse
import pandas as pd
import re
import os
import datetime
import logging
logging.basicConfig(filename='scrapelog.txt', filemode='w', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
#logging.getLogger().addHandler(logging.StreamHandler())

def getattr(tag,attr):
   if tag.has_attr(attr):
      return tag[attr]
   else:
      return None
      
def gettext(tag):
   if tag is None:
      return None
   else:
      return tag.text.strip() 

# Build list of 10 pages
urlinput = 'https://www.autotrader.co.uk/car-search?sort=relevance&postcode=g690be&radius=1500&make=AUDI&model=A6%20SALOON&include-delivery-option=on'
re_url = re.search('autotrader.co.uk/',urlinput)
urlbase = urlinput[:re_url.end()]
urlsearch = urlinput[re_url.end():]
#print(urlbase)
#print(urlsearch)

numpages = 100
pagerange = range(2, numpages+1)

urllist = [urlbase + urlsearch + f'&page={int(x)}' for x in pagerange]
urllist.insert(0,urlbase + urlsearch)
#print(urllist)
#raise Exception

# Request page content
print(f'Scraping {numpages} pages on base url {urlinput}\n')
logging.info(f'Scraping {numpages} pages on base url {urlinput}')
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
page = requests.get(urllist[0], headers=headers)
wait=1
time.sleep(wait)

soupindex = BeautifulSoup(page.content, 'html.parser')

thisurl = urllist[0]

detail = False

for i, thisurl in enumerate(urllist):
   print(f'Page {i+1} of {len(urllist)}')

   page = requests.get(thisurl, headers=headers)
   wait = 1
   time.sleep(wait)

   # Find attributes for each product result 
   soup = BeautifulSoup(page.content, 'html.parser')
   s_results = soup.find('div', class_='search-page__results')
   #ads = s_results.find('li', class_='search-page__result')
   logging.info(f'Scraping page {i} of {numpages}')
   
   df = pd.DataFrame()

   for j, t in enumerate(s_results.find_all('li', class_='search-page__result')):
      if j>=20:
         continue

      d_advert_id = getattr(t,'data-advert-id')
      d_distance_value = getattr(t,'data-distance-value')
      d_data_condition_value = getattr(t,'data-condition-value')
      d_good_great_value = getattr(t,'data-good-great-value')
      d_has_finance = getattr(t,'data-has-finance')
      d_image_count = getattr(t,'data-image-count')
      d_is_allocated_stock = getattr(t,'data-is-allocated-stock')
      d_is_franchise_approved = getattr(t,'data-is-franchise-approved')
      d_is_group_stock = getattr(t,'data-is-group-stock')
      d_is_manufacturer_approved = getattr(t,'data-is-manufacturer-approved')
      d_is_multi_location_advert = getattr(t,'data-is-multi-location-advert')
      d_is_network_stock = getattr(t,'data-is-network-stock')
      d_is_virtual_stock = getattr(t,'data-is-virtual-stock')
      d_search_results_advert_card = getattr(t,'data-search-results-advert-card')
      d_id = getattr(t,'id')

      d_price = gettext(t.find('div', class_='product-card-pricing__price'))

      d_title = gettext(t.find('h3', class_='product-card-details__title'))

      d_detail = gettext(t.find('p', class_='product-card-details__subtitle'))

      d_attention_grabber = gettext(t.find('p', class_='product-card-details__attention-grabber'))

      ul = t.find('ul', class_='listing-key-specs').find_all('li')
      d_key_spec_list = [x.text.strip() for x in ul]

      d_seller_private_trade = gettext(t.find('h3', class_='product-card-seller-info__name'))

      d_seller_location = gettext(t.find('span', class_='product-card-seller-info__spec-item-copy'))

      if detail==True:
         urldetail = urlbase + f'car-details/{d_id}?'
         pagedetail = requests.get(urldetail, headers=headers)
         wait = 1
         time.sleep(wait)

         soupdetail = BeautifulSoup(pagedetail.content, 'html.parser')
         d_title_full = soupdetail.find('meta', attrs={'name':'og:title'})['content']
         d_description_full = soupdetail.find('meta', attrs={'name':'og:description'})['content']
      else:
         d_title_full = 'skip'
         d_description_full = 'skip'
     
      # Store to dict
      d_dict = {'advert_id':d_advert_id,
         'distance_value':d_distance_value,
         'condition_value':d_data_condition_value,
         'good_great_value':d_good_great_value,
         'has_finance':d_has_finance,
         'image_count':d_image_count,
         'is_allocated_stock':d_is_allocated_stock,
         'is_franchise_approved':d_is_franchise_approved,
         'is_group_stock':d_is_group_stock,
         'is_manufacturer_approved':d_is_manufacturer_approved,
         'is_multi_location_advert':d_is_multi_location_advert,
         'is_network_stock':d_is_network_stock,
         'is_virtual_stock':d_is_virtual_stock,
         'search_results_advert_card':d_search_results_advert_card,
         'id':d_id,
         'price':d_price,
         'title_ad':d_title,
         'detail_ad':d_detail,
         'attention_grabber':d_attention_grabber,
         'key_spec_list_ad':d_key_spec_list,
         'seller_private_trade':d_seller_private_trade,
         'seller_location':d_seller_location,
         'title_full':d_title_full,
         'description_full':d_description_full,
         'time_of_scrape':datetime.datetime.now()}

      df = df.append(d_dict, ignore_index=True)

      print(f'   {d_id}, {d_price:10}, {d_key_spec_list[0]:5}, {d_key_spec_list[2]}')
      
   if os.path.isfile('scraped_autotrader.csv'):
      df.to_csv('scraped_autotrader.csv', index=False, mode='a', header=False)
      print(f'df appended to {os.path.join(os.getcwd(),"scraped_autotrader.csv")}')
      logging.info('Appended df to file')
   else:
       df.to_csv('scraped_autotrader.csv', index=False)
       print(f'Saved df to newfile {os.path.join(os.getcwd(),"scraped_autotrader.csv")}')
       logging.info('Saved df to newfile')
       
logging.info('Finished processing script')
#print(df.head(1).T)
