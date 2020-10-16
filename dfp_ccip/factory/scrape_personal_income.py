'''
    File name: scrape_personal_income
    Group members: Kiana, Xiaoye, Joe
    Purpose: Scrape personal income data
'''
import json
from urllib.request import urlopen
import pandas as pd


# Load BEA data as personal income
# UserID = 322A22BC-16BF-4169-B16A-F52741FC84A2
with urlopen('https://apps.bea.gov/api/data/?UserID=322A22BC-16BF-4169-B16A-F52741FC84A2'
             '&method=GetData&datasetname=Regional&TableName=CAINC1&LineCode=1&Year=2018,2019'
             '&GeoFips=COUNTY&ResultFormat=json') as response:
    source = response.read().decode('utf-8', 'ignore') # Had to specify to ignore certain characters that could not be decoded
data = json.loads(source)

# Create dataframe
pi_df = pd.DataFrame(data['BEAAPI']['Results']['Data'])

# Function for calling dataframe in other module
def get_pi_df():
    return pi_df
        


