# -*- coding: utf-8 -*-
"""wrangling_project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1w1tj08SEXCkazLcw7FB2_JF3QW4Y9vs7

data wrangling of stock market
"""

import requests
from bs4 import BeautifulSoup
import time
import csv
import glob
import openpyxl



"""collection of data through web scraping:-"""

# trying to access the each stock link from most-active stock list in a website
stocks_url = 'https://www.moneycontrol.com/stocks/marketstats/bse-mostactive-stocks/bse-100-1/'

response = requests.get(stocks_url)

response.status_code

doc = BeautifulSoup(response.text, 'lxml')
doc

table=doc.find_all('td',class_='PR')
table

selection_class = 'gld13 disin'

span_tags = doc.find_all('span',{
                                    'class' : selection_class
})

span0 = span_tags[0]

a_tags0 = span0.findChild()

a_tags0

a_tags0.text

a_url = a_tags0['href']
print(a_url)

company_names = []
for span in span_tags:
    a = span
    a_tag = a.findChild().text
    company_names.append(a_tag)
print(company_names)
print(len(company_names))

stock_url = []
for span in span_tags:
    a = span
    a_tag = a.findChild()
    a_url = a_tag['href']
    stock_url.append(a_url)
print(stock_url)

#dataframe has been created for evry stock and its url
stock_dict = {'Name' : company_names,
              'URL'  : stock_url }
import pandas as pd
stock_df = pd.DataFrame(stock_dict)

stock_df.head()

#extracting required data from each stock

stock_info_dict = {
    'Stock_Name' : [],
    'open' : [],
    'Previous_Close' : [],
    'High' : [],
    'Low' : [],
    'Sector_PE' : [],
    'Book_Value' : [],
    'Dividend_Yield' : []
    }

def stock_extract(stocks_url):
  response = requests.get(stocks_url)
  response.status_code
  stock_info = BeautifulSoup(response.text, 'html.parser')
  div_class = 'inid_name'
  stock_name_tag = stock_info('div', {'class'  : div_class})
  name_stock = stock_name_tag[0]
  stock_name = name_stock.findChild().text
  print(stock_name)
  openl = stock_info.find('td', {'class' :'nseopn bseopn' }).text.strip()
  print(openl)
  pc =  stock_info.find('td', {'class' :'nseprvclose bseprvclose' }).text.strip()
  print(pc)
  high =  stock_info.find('td', {'class' :'nseHP bseHP' }).text.strip()
  print(high)
  low =  stock_info.find('td', {'class' :'nseLP bseLP'}).text.strip()
  print(low)
  sec_pe =  stock_info.find('td', {'class' :'nsesc_ttm bsesc_ttm'}).text.strip()
  print(sec_pe)
  bv =  stock_info.find('td', {'class' :'nsebv bsebv' }).text.strip()
  print(bv)
  dy =  stock_info.find('td', {'class' :'nsedy bsedy'}).text.strip()
  print(dy)
  stock_info_dict['Stock_Name'].append(stock_name)
  stock_info_dict['open'].append(openl)
  stock_info_dict['Previous_Close'].append(pc)
  stock_info_dict['High'].append(high)
  stock_info_dict['Low'].append(low)
  stock_info_dict['Sector_PE'].append(sec_pe)
  stock_info_dict['Book_Value'].append(bv)
  stock_info_dict['Dividend_Yield'].append(dy)
  return stock_info_dict

for i in range (len(stock_url)):
  stock=stock_extract(stock_url[i])

import pandas as pd
df=pd.DataFrame(stock)
df

df.to_excel('stock3.xlsx',index=False)#save the unstructured data into excel file

"""cleaning of data"""

df2=pd.read_excel("/content/stock3.xlsx")
df2

df2.dtypes

columns=df2[['Previous_Close','open','High','Low','Book_Value']]
# Loop through each column and convert to string, then replace characters      df2[col] = df2[col].str.replace(',', '', regex=True)  # Remove commas
# Print the DataFrame to verify the conversion

import pandas as pd

# Loop through each column and convert to string if not already, then replace characters
for col in columns:
    if df2[col].dtype != 'object':  # Check if the column is not already of object (string) data type
        df2[col] = df2[col].astype(str)  # Convert the column to string

    df2[col] = df2[col].str.replace(',', '', regex=True)  # Remove commas

    df2[col] = pd.to_numeric(df2[col], errors='coerce')  # Convert to float, replacing non-numeric values with NaN

# Print the DataFrame to verify the conversion

df2.dtypes

df2.head()

df2.isna().sum()

df2['Book_Value'].values

df2.fillna(0).inplace=True

df2.describe()

df2.to_excel('stocks_final.xlsx',index=False)#save the structured data into excel file

df41=pd.read_excel("/content/stocks_final.xlsx")
df41.head()

df41.dtypes

"""EDA"""

df41.isnull().sum()

import pandas as pd
import klib
import matplotlib.pyplot as plt
import seaborn as sns

klib.corr_mat(df41)

klib.corr_plot(df41)

klib.corr_interactive_plot(df41,split="neg").show()

klib.dist_plot(df41)

klib.missingval_plot(df41)

import seaborn as sns
sns.barplot(df41)

sns.lineplot(df41)

plt.hist(df41['open'])
plt.show()

sns.scatterplot(x='stock_name', y='previous_close', data=df41)
plt.show()

sns.barplot(x='stock_name', y='previous_close', data=df41)
plt.show()

pip install pandas_profiling

import pandas_profiling

pandas_profiling.ProfileReport(df, title="Pandas Profiling Report", explorative=True)

"""**CONCLUSION**
with the help of this dataset we can get to know the information of intraday stocks which are most active on that particular day. this further will give good idea about the stocks to invest
"""

