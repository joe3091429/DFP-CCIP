#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 13:21:44 2020

@author: kianaocean
"""

import pandas as pd
from datetime import date
from datetime import timedelta


csv_path = 'county_level_merge.csv'
df = pd.read_csv(csv_path, thousands=',')

csv_path = 'demographic_data.csv'
demo_df = pd.read_csv(csv_path)

# Set today and yesterday dates
today = date.today()
yesterday = today - timedelta(days = 1)

county = input("Enter your county name: ")
state = input("Enter your state name: ")

if ((county == '') & (state == '')):
    pop = int(demo_df['total_population'].sum())
    df['date'] = pd.to_datetime(df['date'])
    max_date = df['date'].max()
    cases = (df.loc[df.date == max_date, 'cases'].sum()) - \
        (df.loc[df.date == (max_date-timedelta(days=14)), 'cases'].sum())
    deaths = (df.loc[df.date == max_date, 'deaths'].sum()) - \
        (df.loc[df.date == (max_date-timedelta(days=14)), 'deaths'].sum())
    
    df = df[['county','state','civ_labor_force','unemployed','date_monthly']]
    df.drop_duplicates(inplace=True)
    
    df['date_monthly'] = pd.to_datetime(df['date_monthly'])
    max_date = df['date_monthly'].max()
    labor_force = df.loc[df.date_monthly == max_date, 'civ_labor_force'].sum()
    num_unemployed = df.loc[df.date_monthly == max_date, 'unemployed'].sum()
    unemployment = (num_unemployed/labor_force)*100
    print('Summary for the United States')
elif (county == ''):
    filter_df = df.loc[df['state'] == state.title()]
    demo_filter_df = demo_df.loc[demo_df['state'] == state.title()]
    pop = int(demo_filter_df['total_population'].sum())
    filter_df['date'] = pd.to_datetime(filter_df['date'])
    max_date = filter_df['date'].max()
    cases = (filter_df.loc[filter_df.date == max_date, 'cases'].sum()) - \
        (filter_df.loc[filter_df.date == (max_date-timedelta(days=14)), 'cases'].sum())
    deaths = (filter_df.loc[filter_df.date == max_date, 'deaths'].sum()) - \
        (filter_df.loc[filter_df.date == (max_date-timedelta(days=14)), 'deaths'].sum())
    
    filter_df = filter_df[['county','state','civ_labor_force','unemployed','date_monthly']]
    filter_df.drop_duplicates(inplace=True)
    
    filter_df['date_monthly'] = pd.to_datetime(filter_df['date_monthly'])
    max_date = filter_df['date_monthly'].max()
    labor_force = filter_df.loc[filter_df.date_monthly == max_date, 'civ_labor_force'].sum()
    num_unemployed = filter_df.loc[filter_df.date_monthly == max_date, 'unemployed'].sum()
    unemployment = (num_unemployed/labor_force)*100
    print('Summary for the state of',state.title())
else:
    filter_df = df.loc[(df['county'] == county.title()) & (df['state'] == state.title())]
    pop = int(filter_df['total_population'].max())
    filter_df['date'] = pd.to_datetime(filter_df['date'])
    filter_df.sort_values(by=['date'], inplace=True)
    num_rows, num_cols = filter_df.shape
    cases = (filter_df.iloc[num_rows-1]['cases']) - (filter_df.iloc[num_rows-15]['cases'])
    deaths = (filter_df.iloc[num_rows-1]['deaths']) - (filter_df.iloc[num_rows-15]['deaths'])
    
    filter_df['date_monthly'] = pd.to_datetime(filter_df['date_monthly'])
    max_date = filter_df['date_monthly'].max()
    unemployment = filter_df.loc[filter_df.date_monthly == max_date, 'unemployed_rate'].max()
    
    print('Summary for',county.title(),'County,',state.title())


# Print formatted table
print_dict = {}
print_dict['Total population:'] = pop
print_dict['Unemployment rate last reported month:'] = unemployment
print_dict['New Covid-19 cases in last 14 days:'] = cases
print_dict['    per 100,000:'] = (cases*100000)/pop
print_dict['Covid-19 deaths in last 14 days:'] = deaths
for key, value in print_dict.items():
    if ((key == 'Total population:')|(key == 'New Covid-19 cases in last 14 days:')|(key == 'Covid-19 deaths in last 14 days:')):
        print(f'{key:40}{value:,}')
    elif ((key == 'Unemployment rate last reported month:')|(key == '    per 100,000:')):
        print(f'{key:40}{value:.1f}')
    else:
        print(f'{key:40}{value}')

