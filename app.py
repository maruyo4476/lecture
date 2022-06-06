
import streamlit as st
import numpy as np
import pandas as pd
st.title('ハローワークをスクレイピング')   
st.title('するぞ    ！！！') 

st.write('検索条件')
st.write('求人区分　一般求人（フルパート）：雇用形態　正社員')
st.write('新着求人　新着（1週間以内）の求人情報から検索')
citys=None
mydict={"高浜市":"23227","岡崎市":"23202","安城市":"23212","刈谷市":"23210","豊田市":"23211","碧南市":"23209"} 
citys=st.selectbox('市名を選択してください。',('高浜市','岡崎市','安城市','刈谷市','豊田市','碧南市'))
if citys is not None:
    
    button=st.button('検索開始')
    comment=st.empty()
    st.subheader('検索は少し時間が掛かります。')


#from selenium import webdriver
#import os, sys

#@st.experimental_singleton
#def installff():
#  os.system('sbase install webdriver')
#  os.system('ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/drivers/webdriver /home/appuser/venv/bin/webdriver')

#_ = installff()

##from selenium.webdriver import FirefoxOptions
##opts = FirefoxOptions()
##opts.add_argument("--headless")
##browser = webdriver.Firefox(options=opts)

##browser.get('http://example.com')


#from webdriver_manager.chrome import ChromeDriverManager


#import streamlit as st
import os, sys

@st.experimental_singleton
def installff():
  os.system('sbase install geckodriver')
  os.system('ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/drivers/geckodriver /home/appuser/venv/bin/geckodriver') 
_ = installff()
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
opts = FirefoxOptions()
opts.add_argument("--headless")
#driver=webdriver.Firefox(exectable_path=firefox_driver_path)
driver= webdriver.Firefox(options=opts)
import re
import requests

from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.chrome.options import Options
#options=Options()
#options.add_argument('--headless')
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

from requests.exceptions import Timeout
#driver=webdriver.Chrome(ChromeDriverManager().install(),options=options)


url='https://www.hellowork.mhlw.go.jp/'
driver.get(url)
#driver.get(url)
time.sleep(1)
elem_kyuujin_btn=driver.find_element_by_class_name('retrieval_icn')
elem_kyuujin_btn.click()
time.sleep(1)
terms=driver.find_element_by_id('ID_ippanCKBox1')
terms.click()
time.sleep(1)
element =driver.find_element_by_id('ID_tDFK1CmbBox')
Select(element).select_by_value('23')
time.sleep(1)
driver.find_element_by_id('ID_Btn').click()
time.sleep(1)
element=driver.find_element_by_id('ID_rank1CodeMulti')
Select(element).select_by_value(mydict[citys])
time.sleep(1)
driver.find_element_by_id('ID_ok').click()
time.sleep(1)
terms=driver.find_element_by_id('ID_koyoFltmCKBox1')
terms.click()
time.sleep(1)
terms=driver.find_element_by_id('ID_newArrivedCKBox2')
terms.click()
time.sleep(1)

driver.find_element_by_id('ID_searchBtn').click()
time.sleep(1)
element =driver.find_element_by_id('ID_fwListNaviDispTop')
Select(element).select_by_value('50')
time.sleep(1)


keys=[]
soup=BeautifulSoup(driver.page_source,'html.parser')
elems=soup.find_all('a',attrs={'id':'ID_dispDetailBtn'})
import re


for elem in elems:
        _keys=[]
        elem=elem.get('href')
        elem=elem.replace('./','',1)
        url='https://www.hellowork.mhlw.go.jp/kensaku/'
        url=url+elem


        res=requests.get(url,timeout=(3.0,7.5))
                
        soup=BeautifulSoup(res.text,'html.parser')
            
        elem=soup.find('div',attrs={'name':'kjNo'})

        elem=elem.text
        _keys.append(elem)
        elem=soup.find('div',attrs={'id':'ID_jgshMei'})
        if not elem:
            elem='あきまへんわ'
            _keys.append(elem)
        else:
            elem=elem.text
            elem=re.sub('[\r\u3000]','',elem)
            _keys.append(elem)
        elem=soup.find('div',attrs={'id':'ID_szciYbn'})
        if not elem:
            elem='あきまへんわ'
            _keys.append(elem)
        else:
            elem=elem.text
            elem= re.sub('[\r\u3000]','',elem)
            _keys.append(elem)
        elem=soup.find('div',attrs={'id':'ID_szci'})
        if not elem:
            elem='あきまへんわ'
            _keys.append(elem)
        else:
            elem=elem.text
            elem= re.sub('[\r\u3000]','',elem)
            _keys.append(elem)
        elem=soup.find('div',attrs={'id':'ID_shgBsYubinNo'})
        if not elem:
            elem='あきまへんわ'
            _keys.append(elem)
        else:
            elem=elem.text
            elem=re.sub('[\r\u3000]','',elem)
            _keys.append(elem)
        elem=soup.find('div',attrs={'id':'ID_shgBsJusho'})
        if not elem:
            elem='あきまへんわ'
            _keys.append(elem)
        else:
            elem=elem.text
            elem=re.sub('[\r\u3000]','',elem)
            _keys.append(elem)
        keys.append(_keys)  
import pandas as pd
df=pd.DataFrame()
df_keys=pd.DataFrame(keys)
df_keys.columns=['求人番号','事業所名','〒本社','本社住所','〒勤務先','勤務先住所']
duplicated_df=df_keys.drop_duplicates(subset=['事業所名'])
duplicated_df=duplicated_df[duplicated_df['事業所名'] != 'あきまへんわ']
duplicated_df.reset_index(drop=True,inplace=True)

st.table(duplicated_df)
