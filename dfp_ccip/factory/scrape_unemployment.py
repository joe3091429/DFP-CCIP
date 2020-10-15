from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from dfp_ccip.factory import state_abbrvs

# Scrape unemployment data from BLS website and export to dataframe and csv

# Scrape data from BLS site and write to txt file
html = urlopen('https://www.bls.gov/web/metro/laucntycur14.txt')
bsyc = BeautifulSoup(html.read(), "lxml")
fout = open('data/unemployment_raw.txt', 'wt', encoding='utf-8')
fout.write(str(bsyc))
fout.close()

# Clean data and convert to dataframe
fin = open('data/unemployment_raw.txt')
dict = {}
i = 0
for line in fin:
    if line[1:2] == 'C':
        field = line.split(sep='|')
        field_clean = []
        for f in field:
            field_clean.append(f.strip())
        dict[i] = field_clean
        i += 1
        
col_names = ['area_code', 'state_fips', 'county_fips', 'area_title', 'period',\
             'civ_labor_force', 'employed', 'unemployed', 'unemployed_rate']
ue_df = pd.DataFrame.from_dict(dict, orient='index', columns=col_names)

# Create FIPS code column in unemployment data
ue_df['fips'] = ue_df['state_fips'] + ue_df['county_fips']

# Clean and reformat date
date_list = []
month_list = []
year_list = []
num_rows, num_cols = ue_df.shape
for i in range(num_rows):
    clean_date = ue_df.iloc[i]['period'].replace('(p)', '')
    date = datetime.strptime(clean_date, '%b-%y')
    month = date.month
    year = date.year
    date_list.append(date)
    month_list.append(month)
    year_list.append(year)
ue_df['date_monthly'] = date_list
ue_df['month'] = month_list
ue_df['year'] = year_list

# Split county name/state and clean county names
new = ue_df['area_title'].str.split(', ', n=1, expand=True)
ue_df['county'] = new[0]
ue_df.replace({'county': r'County$|Borough/city$|Borough$|Census Area$|Borough/municipality$|Municipality$|'
              'County/city$|Parish$|County/town$|city$|Municipio$'},\
              {'county': ''}, regex=True, inplace=True)
ue_df.replace({'county': r' $'}, {'county': ''}, regex=True, inplace=True) # gets rid of trailing space
ue_df['state_abbrv'] = new[1]
state_df = state_abbrvs.get_df()
ue_df = pd.merge(ue_df, state_df, how='left', on=['state_abbrv'])

# Export to CSV
ue_df.to_csv('data/unemployment.csv', index=None)

# Function for calling dataframe in merge module
def get_ue_df():
    return ue_df



