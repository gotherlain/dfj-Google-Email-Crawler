import pandas as pd
import os
import http
import urllib2
import httplib
from bs4 import BeautifulSoup
import re
import socket
import requests
from googlesearch import search
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor

def ask_user(question):
    response = input(question + 'y/n' + '\n')
    if response == 'y':
        return True
    else:
        return False

def create_file(path):
    response = False
    if os.path.exists(path):
        response = ask_user('File already exists, replace?')
        if response == False: return 
    
    with open(path, 'wb') as file: 
        file.close()


# timeout in seconds
timeout = 5
socket.setdefaulttimeout(timeout)

#proxy_handler = urllib2.ProxyHandler({'http': 'http://81.95.226.138:3128'})
#proxy_auth_handler = urllib2.ProxyBasicAuthHandler()
#proxy_auth_handler.add_password('realm', 'host', 'username', 'password')
realUrl=""
lk=0

path = './ioGestd.csv'
create_file(path)
df = pd.DataFrame(columns=['Email', 'Pagina', 'Numero','Link'], index=[0])
df.to_csv(path, mode='w', header=True)
#open= urllib2.build_opener(proxy_handler, proxy_auth_handler)
for url in search('Gestao de condominio curitiba',stop=300):
	realUrl = url
	try:
		#create request and set user agent
		request = urllib2.Request(realUrl)#'https://www.google.com/search?q=administradoras+de+condominio+curitiba&num=100')
		request.add_header('User-Agent', 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11')

		#site = 'https://www.google.com/search?q=administradoras+de+condominio+curitiba&num=100'
		#session = requests.Session()
		#headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'}

		#page.add_header('User-agent', )
		#open page
		#proxy={'https':"socks5://184.82.128.211:8080"}

		#open = requests.get(site,headers=headers,proxies=proxy)
		try:
			open = urllib2.urlopen(request)
		except:
			continue
		page = BeautifulSoup(open, 'html5lib')
		try:
			title = page.title.text #title of page

			print title
		except:
			continue

		regx = '\w+@\w+\.{1}\w+'
		#for x in page.find_all('a'):     
		regNum = '(\(?\d{2}\)?\s)?(\d{4,5}\-\d{4})'					#for d in x.find_all('span',class_ = 'fYyStc'): 
		    #  links_with_text.append(a['href'])
		 		#i+=1
		paragraphs2 = re.findall(regx,str(page))
		 		#print b.contents[0]
		numeros = re.findall(regNum,str(page))        			
		for eachP2 in paragraphs2:
			lk =lk+1
			#if eachP2 == True:					#aux = eachP2				#if eachP2 != aux:
			#title = page.title.text 
			print eachP2

			for numero in numeros:
				#print numero
        	#dic = {'email': eachP2, 'link': title} index=[0.encode('utf-8')]
        			df = pd.DataFrame({'Email': eachP2, 'Pagina': realUrl,'Numero':str(numero), 'Link': title.encode('utf-8') }, index=[0])
        
        			df.to_csv(path, mode='a', header=False)
        			df.to_csv(path, mode='a', header=False)
			
	
	except ValueError as e:
			print e
			#			continue
			pass
	except socket.error:
	     			#ex = None;
	     	continue

	except httplib.BadStatusLine:
	        pass

df = pd.read_csv(path, index_col=0)
df.columns = ['Email', 'Pagina', 'Numero', 'Link']
#df = df.drop_duplicates(subset='pagina')
df = df.drop_duplicates(subset='Email')

df = df.reset_index(drop=True)
df.to_csv(path, mode='w', header=True)	        
print lk