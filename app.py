import streamlit as st
import pandas as pd
import logging
from onpage import Onpage  

logging.basicConfig(filename='test.log')
st.set_page_config(
   page_title="Obtener valores onpage de una lista de URL: title, h1/2/3/4/5/6 (tal cuál están en la URL)",
   layout="wide"
)
st.title("Obtener valores onpage de una lista de URL: title, h1/2/3/4/5/6 (tal cuál están en la URL)")

#Elimina los duplicados de una lista
def eliminaDuplicadosLista(lista):
    if len(lista)>0:
        lista=list(dict.fromkeys(lista))
    return lista

lista_url=st.text_area("Introduzca las URL que desea analizar o cárguelas en un CSV",'')
csv=st.file_uploader('CSV con las URL a analizar', type='csv')
addresses=[]
#Si no hay CSV miramos el textArea
if csv is  None:
    if len(lista_url)>0:
        addresses=lista_url.split('\n')
else: 
    df_entrada=pd.read_csv(csv,header=None)
    st.write(df_entrada)
    addresses = df_entrada[0].tolist()
if len(addresses)>0:
    df_final = pd.DataFrame([])
    #Eliminamos posibles duplicados
    lista=eliminaDuplicadosLista(addresses)
    total_count=0
    bar = st.progress(0.0)
    longitud=len(lista)
    for row in lista:
        total_count+=1
        percent_complete=total_count/longitud
        bar.progress(percent_complete)
        op=Onpage(row)
        df=op.toDataframe()
        df_final=pd.concat([df_final,df])
    st.write(df_final)
    st.download_button(
        label="Descargar como CSV",
        data=df_final.to_csv(index=False, decimal=",",quotechar='"').encode('utf-8'),
        file_name='onpage.csv',
        mime='text/csv'
        )
else:
    st.warning("No ha introducido ninguna URL") 