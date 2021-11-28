from bs4 import BeautifulSoup
import requests
import pandas
from datetime import date
from datetime import datetime
import boto3

s3 = boto3.resource('s3')

url = "https://www.eltiempo.com/"
url2 = "https://www.publimetro.co/"

#Día actual
today = date.today()

#Fecha actual
now = datetime.now()

dia = today.day
mes= today.month
año = today.year 

page = requests.get(url)
page2 = requests.get(url2)

soup = BeautifulSoup(page.content, 'html.parser')
soup2 = BeautifulSoup(page.content, 'html.parser')

fecha = soup2.find('div', class_='fecha').getText()
    
#dia = fecha[16:19]
#año = '2021'
#mes = '11'

def eltiempo():
    htmlpage= open('/tmp/eltiempo.html', 'w')
    htmlpage.write(str(soup))
    htmlpage.close()

def publimetro():
    htmlpage= open('/tmp/publimetro.html', 'w')
    htmlpage.write(str(soup))
    htmlpage.close()

eltiempo()
publimetro()

s3.meta.client.upload_file('/tmp/eltiempo.html', 'miperiodico007v2',
                            f'headlines/raw/periodico=ElTiempo/year={año}/month={mes}/day={dia}/eltiempo.html')
                                
                    
s3.meta.client.upload_file('/tmp/publimetro.html', 'miperiodico007v2',
                            f'headlines/raw/periodico=Publimetro/year={año}/month={mes}/day={dia}/publimetro.html')