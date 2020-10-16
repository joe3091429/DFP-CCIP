'''
    File name: scrape_demo_social
    Group members: Kiana, Xiaoye, Joe
    Purpose: Merge demographic and social data
'''
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests as rq
import lxml

def ScrapeDS():

    tb_data = []
    tb_title = []
    sh_table_list = []

    url = "https://www.pewresearch.org/internet/fact-sheet/internet-broadband/"
    html = urlopen(url)
    bsyc = BeautifulSoup(html.read(), "lxml")
    tr_table_list = bsyc.findAll('tr')

    for row in tr_table_list:
        cols=row.find_all('td')
        cols=[x.text.strip() for x in cols]
        tb_data.append(cols)

    for row in tr_table_list:
        cols=row.find_all('th')
        cols=[x.text.strip() for x in cols]
        if cols != []:
            tb_title.append(cols) 

    # combine title and data in one sample
    for i in range(0,20):
        if tb_data[i] != []:
            sh_table_list.append(tb_data[i])

    sh_table = pd.read_csv('data/us_county_sociohealth_data.csv')
    sh_table['fips'] = sh_table['fips'].map("{:05}".format)
    sh_table.to_csv('data/demographic_data.csv', index = False)
    return