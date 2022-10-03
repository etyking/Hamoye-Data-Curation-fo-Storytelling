import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
from time import sleep

headers = {
    'Host': 'www.amazon.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,/;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Cookie': 'session-id=131-8633176-9766657; session-id-time=2082787201l; i18n-prefs=USD; csm-hit=tb:D394FZ5QA7KQQ48TVTZA+s-33H4GRPEWQ6ENXJJ74S8|1664452474237&t:1664452929801&adb:adblk_no; ubid-main=132-4615754-8330846; session-token=mvNgLfS9mnwg2dnyNdKsP2BcW+Iqv6FeiqzRQMSexe5zaZtFuLGCZVtUKbWkwsBKFPAcXtKrVu0NGsZUZ/BFvgMabW6l3WbDAjKe5K8uyjZEpES/x+XjKUbLVAOUb0bsJmZkkTDgDD+IB5EPNqe9/QKw/qnkb+VWG9ugggMYUWYqNnhrridxGtQ5eD59qOcqs8w1Y2t1m4rDElNiSht2yb28AbA4DVlK; sp-cdn="L5Z9:GH"; skin=noskin',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'TE': 'trailers'
	
}


search_query = 'https://www.amazon.com/s?k=amazon+shopping+online&rh=n%3A283155&dc&adgrpid=84486094307&gclid=CjwKCAjwwab7BRBAEiwAapqpTDYtTN8aym2q_rlYn1VdmofKw0_bzkd6xjaCl8cMY4syjbPZMKNMjxoCLIYQAvD_BwE&hvadid=393524136919&hvdev=c&hvlocphy=1010294&hvnetw=g&hvqmt=b&hvrand=2170543926145783317&hvtargid=kwd-469356929&hydadcr=22365_10729094&qid=1600780278&rnid=2941120011&tag=hydglogoo-20&ref=sr_nr_n_10'
Books = []
for i in range(1,76):
    print('Processing {0}...'.format(search_query + '&page={0}'.format(i)))
    response = requests.get(search_query + '&page={0}'.format(i), headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    print(response)
    # print(soup)
    
    results = soup.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})
    for result in results:
        bookName = result.h2.text

        try:
            datePub = result.find('span', {'class': 'a-size-base a-color-secondary a-text-normal'}).text
        except AttributeError:
            continue
        try:
            type= result.find('a', {'class': 'a-text-bold'}).text
        except AttributeError:
            continue 

        try:
            rate= result.find('span', {'class': 'a-size-base s-underline-text'}).text
            
            Books.append([bookName, type, datePub, rate])
        except AttributeError:
            continue          
        # print('Type:',rate)
        # break
    sleep(1.0)

    df = pd.DataFrame(Books, columns=['BookName', 'Type', 'Date', 'Rate'])
    df.to_csv('Amazon Books.csv', index=False)