
# coding: utf-8

# In[1]:


import urllib.request
from lxml import etree
import pandas as pd
import calendar
import datetime


# In[2]:


def parseDate(date, dateResult):
    # the address of the exchange rate site page
    url = "https://www.x-rates.com/historical/?from=SGD&amount=1&date="
    url += date
    with urllib.request.urlopen(url) as response:
       page_content = response.read()

    ## Parse HTML data
    html = etree.HTML(page_content)
    html_table1 = html.find('.//table[@class="ratesTable"]/tbody')
    for row in html_table1:
        country = row.find('.//td')
        exchange_rate = row.findall('.//td[@class="rtRates"]/a')
        country_result = {'Date': date,'Country': country.text, '1.00 SGD': exchange_rate[0].text, 'inv. 1.00 SGD': exchange_rate[1].text}
        dateResult.append(country_result)
    html_table2 = html.find('.//table[@class="tablesorter ratesTable"]/tbody')
    for row in html_table2:
        country = row.find('.//td')
        exchange_rate = row.findall('.//td[@class="rtRates"]/a')
        country_result = {'Date': date,'Country': country.text, '1.00 SGD': exchange_rate[0].text, 'inv. 1.00 SGD': exchange_rate[1].text}
        dateResult.append(country_result)
    
    return dateResult

        
        
        
        


# In[4]:


# conver to DataFrame
# we would like to parse data all the way till 2013-01-01
parsedData = []
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)
        
start_date = datetime.date(2008, 11, 1)
end_date = datetime.date(2018, 11, 4)
for single_date in daterange(start_date, end_date):
    date = single_date.strftime("%Y-%m-%d")
    parsedData = parseDate(date, parsedData)

data = pd.DataFrame(parsedData)
data.to_csv("exchange-rate-data-to-2008-11-1.csv", index=False)

