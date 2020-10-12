## Personal income
import json
from urllib.request import urlopen
import csv
import pandas as pd
import sys


# Load BEA data as personal income
# UserID = 322A22BC-16BF-4169-B16A-F52741FC84A2
with urlopen('https://apps.bea.gov/api/data/?UserID=322A22BC-16BF-4169-B16A-F52741FC84A2'
             '&method=GetData&datasetname=Regional&TableName=CAINC1&LineCode=1&Year=2018,2019'
             '&GeoFips=COUNTY&ResultFormat=json') as response:
    source = response.read().decode('utf-8', 'ignore') # Had to specify to ignore certain characters that could not be decoded
data = json.loads(source)

# Create dataframe
pi_df = pd.DataFrame(data['BEAAPI']['Results']['Data'])
# print(sys.getsizeof(pi_df))

# Function for calling dataframe in other module
def get_pi_df():
    return pi_df

if __name__ == '__main__':
    # Export to csv
    with open('/Users/kianaocean/Documents/CMU/Python (95888)/Project/personal_income_clean.csv', mode='w') as csv_file:
        fieldnames = ["Code", "GeoFips", "GeoName", "TimePeriod", "CL_UNIT", "UNIT_MULT", "DataValue", "NoteRef"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for item in data['BEAAPI']['Results']['Data']:
            writer.writerow(item)
        


