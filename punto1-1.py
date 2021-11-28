import boto3
from datetime import date
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
import csv

#Día actual
today = date.today()

    #Fecha actual
now = datetime.now()

dia = today.day
mes= today.month
año = today.year

# TODO implement
    
print('archivo recibido')
    
s31 = boto3.client('s3')
s3 = boto3.resource('s3')

bucket = 'miperiodico007v2'
#bucket = event['Records'][0]['s3']['bucket']['name']
#key = event['Records'][0]['s3']['object']['key']
#key = 'eltiempo.html'
    
print(bucket)
    #print(key)
    
#s3.Bucket(bucket).download_file(key, '/tmp/tiempo.html')
s31.download_file(bucket, f'headlines/raw/periodico=ElTiempo/year={año}/month={mes}/day={dia}/eltiempo.html', '/tmp/tiempito.html')
s31.download_file(bucket, f'headlines/raw/periodico=Publimetro/year={año}/month={mes}/day={dia}/publimetro.html', '/tmp/publimetrocito.html')
    
url = '/tmp/tiempito.html'
url1 = '/tmp/publimetrocito.html'

with open('/tmp/tiempito.html') as fp:
    soup = BeautifulSoup(fp, 'html.parser')

with open('/tmp/publimetrocito.html') as fp1:
    soup1 = BeautifulSoup(fp1, 'html.parser')

def tiempo():

    cat = soup.find_all('div', {'class': 'category-published'})
    categorias = list()
    for i in cat:
        categorias.append(i.text)

    tit = soup.find_all('a', {'class': 'title page-link'})
    titulares = list()

    for i in tit:
        titulares.append(i.text)

    links = list()

    for a in soup.find_all('a',{'class': 'multimediatag page-link'}, href=True): 
        if a.text: 
            links.append('https://www.eltiempo.com'+a['href'])

    #df = pd.DataFrame({'Categorias':categorias, 'Titulares':titulares, 'Link':links})
    a = {'Categorias':categorias, 'Titulares':titulares, 'Link':links}
    df = pd.DataFrame.from_dict(a,orient='index')


    #with open('/tmp/Eltiempo.csv', 'w') as f:
        #writer = csv.writer(f)
        #for line in df:
            #writer.writerow(line)

    df.to_csv('/tmp/Eltiempo.csv', index=False)

def publimetro():

        

    cat = soup1.find_all('h4', {'class': 'primary-font__PrimaryFontStyles-o56yd5-0 jqfNWj header-block'})
    categorias = list()
    for i in cat:
        categorias.append(i.text)

    tit = soup1.find_all('h2', {'class': 'primary-font__PrimaryFontStyles-o56yd5-0 jqfNWj headline-text'})
    titulares = list()
    for i in tit:
        titulares.append(i.text)

    link = soup1.find_all('div', {'class': 'results-list--headline-container mobile-order-1'})
    links = list()

    for i in link:
        for a in i.find_all('a', href=True):
            links.append('https://www.publimetro.co/'+a['href'])


    e = {'Categorias':categorias, 'Titulares':titulares, 'Link':links}
    df = pd.DataFrame.from_dict(e,orient='index')


    #with open('/tmp/Publimetro.csv', 'w') as f:
        #writer = csv.writer(f)
        #for line in df:
            #writer.writerow(line)

    df.to_csv('/tmp/Publimetro.csv', index=False)

tiempo()
publimetro()


s3.meta.client.upload_file('/tmp/Eltiempo.csv', 'miperiodico007v2',
                            f'headlines/final/periodico=ElTiempo/year={año}/month={mes}/day={dia}/Tiempo.csv')
                               
s3.meta.client.upload_file('/tmp/Publimetro.csv', 'miperiodico007v2',
                               f'headlines/final/periodico=Publimetro/year={año}/month={mes}/day={dia}/Publimetro.csv')

s3.meta.client.upload_file('/tmp/Eltiempo.csv', 'miperiodico007v2',
                            f'news/raw/periodico=ElTiempo/year={año}/month={mes}/day={dia}/Tiempo.csv')
                               
s3.meta.client.upload_file('/tmp/Publimetro.csv', 'miperiodico007v2',
                               f'news/raw/periodico=Publimetro/year={año}/month={mes}/day={dia}/Publimetro.csv')
#print(open('/tmp/tiempito.html').read())
#s3.meta.client.download_file(bucket, key , 'tiempo.html')