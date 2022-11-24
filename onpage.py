from bs4 import BeautifulSoup
import logging
import ssl
from urllib.request import Request, urlopen
import re
import pandas as pd
#Para que no haya problemas al descargar las imágenes
ssl._create_default_https_context = ssl._create_unverified_context
logging.basicConfig(filename='test.log')


class Heading:
    def __init__(self,tag,text):
        self.tag=tag
        self.text=text
    
    def printHeading(self):
        espacios=""
        if self.tag is not None:
            num=self.tag[1:2]
            i=1
            while i<int(num):
                espacios+="  "
                i+=1
            print(espacios+self.tag+":"+self.text)

class Onpage:
    def __init__(self,url):
        self.url=url
        self.responseUrl=''#por si hay redirección
        self.title=''
        self.headings=[]
        self.status=0
        self.conten_type=""
        self.getOnPage(url)

    def printOnpage(self):
        if self.conten_type=="text/html":
            print("url:"+self.url)
            print("title:"+self.title)
            if len(self.headings)>0:
                for h in self.headings:
                    h.printHeading()
    
    #Compruena si hay datos onpage
    def hayDatos(self):
        hay=False
        if len(self.title)>0:
            hay=True
        return hay

    #Recuepera los valores onpage
    def getOnPage(self,url):
            req = Request(
                url, 
                data=None, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
            )
            response=urlopen(req)
            self.status=response.code
            if response.code==200:
                content_type= response.info().get_content_type()
                self.conten_type=content_type
                self.responseUrl=response.geturl()
                #Si es html podemos obtener los datos onpage
                if content_type=="text/html":  
                    soup = BeautifulSoup(response,"html.parser")
                    title = soup.find('title').get_text().strip()
                    self.title=title
                    headings = soup.find_all(re.compile('^h[1-6]'))
                    l_headings=[]
                    for header in headings:
                        heading=Heading(header.name, header.text.strip())
                        l_headings.append(heading) 
                    self.headings=l_headings
                else:
                    logging.info("No es una página html")
            else:
                logging.info("Código de estado: "+response.code)
        
    
    #Convertimos a DataFrame
    def toDataframe(self):
        resultados=[] 
        df=None
        if self.hayDatos():
            #Añadimos la URL de respuesta por si hay redirección
            resultado={'url':self.url,'tag':'responseUrl','text':self.responseUrl}
            resultados.append(resultado)
            #añadimos title
            resultado={'url':self.url,'tag':'title','text':self.title}
            resultados.append(resultado)
            #añadimos headings
            for heading in self.headings:
                resultado={'url':self.url,'tag':heading.tag,'text':heading.text}
                resultados.append(resultado)
            df=pd.DataFrame(resultados)
        return df