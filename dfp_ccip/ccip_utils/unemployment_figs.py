#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
import json
import pandas as pd
from datetime import datetime
import plotly.express as px
from plotly.offline import plot
import matplotlib.pyplot as plt

class UnemploymentFigs(object):
    '''
        Creates charts and maps of unemployment data (if user chooses economy)
    '''
    def create_economy_data(s_state, s_county):
        
        def clean_fips(df):
            df.rename(columns = {'fips':'fips_old'}, inplace = True)
            num_rows, num_cols = df.shape
            fips_list = []
            for i in range(num_rows):
                fips_clean = str(df.iloc[i]['fips_old']).zfill(5)
                fips_list.append(fips_clean)
            df['fips'] = fips_list
            return df
        
        def make_line_graph(df, area):
            df = df.groupby(['date_monthly']).agg({'civ_labor_force':'sum', 'unemployed':'sum'}).reset_index()
            df['unemployment'] = df['unemployed']/df['civ_labor_force']
            title = 'Unemployment Rate Last 14 Months\n' + area
            df.plot(x='date_monthly', y='unemployment', kind='line', title=title, legend=False)
            plt.show()
            return df
        
        def make_map(df, title, counties):
            fig = px.choropleth(df, geojson=counties, locations='fips', color='unemployed_rate', hover_name='county', title=title,\
                                    color_continuous_scale='Blues', scope='usa', labels={'unemployed_rate':'Unemployment Rate'})
            plot(fig)
            
        
        try:
            # Import base county level map
            with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
                counties = json.load(response)
            
            # Import latest unemployment data CSV & do cleaning
            csv_path = 'data/unemployment.csv'
            df = pd.read_csv(csv_path, dtype={'fips': str, 'area_title': str, 'civ_labor_force': str, \
                                              'employed': str, 'unemployed': str, 'unemployed_rate': str, 'date_monthly': str})
            df = clean_fips(df)
            df = df.loc[df['unemployed_rate'] != '-'] # filter out any missing rates
            df['unemployed_rate'] = pd.to_numeric(df['unemployed_rate'])
            df['civ_labor_force'] = df['civ_labor_force'].str.replace(',', '').astype(float)
            df['unemployed'] = df['unemployed'].str.replace(',', '').astype(float)
            df = df.loc[df['fips'] != '00nan'] # filter out any missing counties
            df['date_monthly'] = pd.to_datetime(df['date_monthly'])
            max_date = df['date_monthly'].max()
            min_date = df['date_monthly'].min()
            
            
            # Get user input
            state = s_state
            county = s_county
            
            continue_option = 'y'
            while (continue_option != 'n'):
                # Get date from user
                date_input = input("Enter month (MM/YYYY) in last 14 months OR 'N/A' for time series: ")
                
                if ((date_input == 'n/a') | (date_input == 'N/a') | (date_input == 'n/A') | (date_input == '')):
                    date_input = 'N/A'
                
                # Filter data based on date provided
                if (date_input != 'N/A'):
                    date = datetime.strptime(date_input, '%m/%Y')
                    
                    if (pd.to_datetime(date) > max_date):
                        date = max_date
                    elif (pd.to_datetime(date) < min_date):
                        date = min_date
                    month_df = df.loc[(df['month'] == date.month) & (df['year'] == date.year)]
                    small_df = month_df.loc[:,['state','county','fips','unemployed_rate','date_monthly','civ_labor_force','unemployed']]
                    small_df.drop_duplicates(inplace=True)
                    
                else:
                    small_df = df.loc[:,['state','county','fips','unemployed_rate','date_monthly','civ_labor_force','unemployed']]
                    small_df.drop_duplicates(inplace=True)
                
                
                # Create maps & plots - outputs one figure depending on user input
                if ((state == '') & (county == '') & (date_input == 'N/A')):
                    output_df = make_line_graph(small_df, 'United States')
                    
                elif ((state != '') & (county == '') & (date_input == 'N/A')):
                    state_df = small_df.loc[small_df['state'] == state]
                    output_df = make_line_graph(state_df, state)
                    
                elif ((state != '') & (county != '') & (date_input == 'N/A')):
                    statecounty_df = small_df.loc[(small_df['state'] == state) & (small_df['county'] == county)]
                    area = county + ' County, ' + state
                    output_df = make_line_graph(statecounty_df, area)
                    
                elif ((state == '') & (county == '') & (date_input != 'N/A')):
                    output_df = small_df
                    date_str = date.strftime('%B %Y')
                    title = 'US Unemployment Rates by County, ' + date_str
                    make_map(small_df, title, counties)
            
                else:
                    state_df = small_df.loc[small_df['state'] == state]
                    output_df = state_df
                    date_str = date.strftime('%B %Y')
                    title = state + ' Unemployment Rates by County, ' + date_str
                    make_map(state_df, title, counties)
                    
                # Download option
                print('Would you like to download this data? (Default as No)\nY) Yes, download it and keep exploring\nN) No, just move on\n')
                load_option = input('Download: ').strip()
                print('')
                if load_option == 'Y' or load_option == 'y':
                    from dfp_ccip.ccip_utils.ccip_utils import CCIPUtils
                    CCIPUtils.download_files(output_df)
                else:
                    print('keep exploring')
                    
                # Continue option
                print('')
                print('Would you like to view more economic data? (Default as Yes)\nY) Yes\nN) No, just move on\n')   
                continue_option = input('Continue?: ')
                if (continue_option == 'n' or continue_option == 'N'):
                    continue_option = 'n'
                else:
                    continue_option = 'y'
                    
            return output_df
        except:
            print('An error has occurred. Please try again.')

            
    if __name__ == "__main__":
        create_economy_data()