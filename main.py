import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
    'Accept-Language': 'en-US, en;q=0.5'
}
boxSetFile = 'box_set_urls'
omnibusFile = 'omnibus_urls'
urlList = []
for i in open(boxSetFile):
    urlList.append(i)
for i in open(omnibusFile):
    urlList.append(i)
volSet = set()
for url in urlList:
    print('-' * 75)
    items = []
    for i in range(1):
        maxStringLength = 50
        urlString = '"{0}"'.format(url)
        if (len(urlString)) > maxStringLength:
            urlString = urlString[0:maxStringLength - 1] + '..."'
        print('Processing {0}...'.format(urlString))
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser') 
        results = soup.find_all('body', {'class': 'a-m-us'})
        for result in results:
            product_name_in = str(result.title)
            name = product_name_in.strip().replace('<title>Amazon.com: ','').replace(': Oda, Eiichiro: Books</title>','').replace('<title>', '').rstrip(': 0123456789')
            nameString = '"{0}"'.format(name)
            if len(nameString) > maxStringLength:
                nameString = nameString[0:maxStringLength - 1] + '..."'
            print('Amazon Listing: {0}'.format(nameString))

            try:
                priceData = result.find('div', {'class': 'a-section aok-hidden twister-plus-buying-options-price-data'}).text
                priceDataList = priceData.split('$')
                priceDataListNextStep = priceDataList[1]
                priceDataListOfList = priceDataListNextStep.split('"')
                priceNum = float(priceDataListOfList[0])
                price = '${:.2f}'.format(priceNum)
                print('Price: {}'.format(price))
                if ('Box Set' in name):
                    if 'East Blue' in name:
                        ppv = priceNum/23
                        numVol = 23
                        volSet.update({1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23})
                    elif 'Skypeia' in name:
                        ppv = priceNum/23
                        numVol = 23
                        volSet.update({24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46})
                    elif 'Thriller Bark' in name:
                        ppv = priceNum/24
                        numVol = 24
                        volSet.update({47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70})
                    elif 'Dressrosa' in name:
                        ppv = priceNum/20
                        numVol = 20
                        volSet.update({71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90})
                    elif 'Omnibus' in name or '-' in name:
                        ppv = priceNum/3
                        numVol = 3
                if '1-2-3' in name:
                    volSet.update({1,2,3})
                elif '4-5-6' in name:
                    volSet.update({4,5,6})
                elif '7-8-9' in name:
                    volSet.update({7,8,9})
                elif '10-11-12' in name:
                    volSet.update({10,11,12})
                elif '13-14-15' in name:
                    volSet.update({13,14,15})
                elif '16-17-18' in name:
                    volSet.update({16,17,18})
                elif '19-20-21' in name:
                    volSet.update({19,20,21})
                elif '22-23-24' in name:
                    volSet.update({22,23,24})
                elif '25-26-27' in name:
                    volSet.update({25,26,27})
                elif '28-29-30' in name:
                    volSet.update({28,29,30})
                print('PPV: ${:.2f}'.format(ppv))
                print('Number Of Volumes: {0}'.format(numVol))
            except AttributeError:
                print('Price: N/A')
                print('PPV: N/A')            
                continue
            break
print(volSet)
