from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import sys


# Scrape data from BLS site and write to txt file
html = urlopen('https://www.bls.gov/web/metro/laucntycur14.txt')
bsyc = BeautifulSoup(html.read(), "lxml")
fout = open('unemployment_raw.txt', 'wt', encoding='utf-8')
fout.write(str(bsyc))
fout.close()


# Clean data and convert to dataframe
fin = open('/Users/kianaocean/Documents/CMU/Python (95888)/Project/unemployment_raw.txt')


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

# Reformat date
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


# print(sys.getsizeof(ue_df))

# Export to CSV
ue_df.to_csv('unemployment.csv', index=None)

# Function for calling dataframe in other module
def get_ue_df():
    return ue_df



