#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 13:21:44 2020

@author: kianaocean
"""

import pandas as pd
from datetime import date
from datetime import timedelta

# Creates summary table for user after they enter state/county

def get_pop(df):
    return int(df['total_population'].sum())

def get_cases(df, yesterday):
    max_date = df['date'].max()
    return (df.loc[df.date == max_date, 'cases'].sum()) - \
        (df.loc[df.date == (yesterday-timedelta(days=14)), 'cases'].sum())
    
def get_deaths(df, yesterday):
    max_date = df['date'].max()
    return (df.loc[df.date == max_date, 'deaths'].sum()) - \
        (df.loc[df.date == (yesterday-timedelta(days=14)), 'deaths'].sum())

def get_unemployment(df):
    df = df[['county','state','civ_labor_force','unemployed','date_monthly']]
    df.drop_duplicates(inplace=True)
    max_month = df['date_monthly'].max()
    labor_force = df.loc[df.date_monthly == max_month, 'civ_labor_force'].sum()
    num_unemployed = df.loc[df.date_monthly == max_month, 'unemployed'].sum()
    return (num_unemployed/labor_force)*100

def get_personal_income(df, pop):
    df = df[['county','state', 'personal_income']]
    df.drop_duplicates(inplace=True)
    income = (df['personal_income'].sum())*1000
    return income/pop

def get_pop_density(df, pop):
    df = df[['county','state', 'area_sqmi']]
    df.drop_duplicates(inplace=True)
    tot_area = df['area_sqmi'].sum()
    return pop/tot_area

def get_num_uninsured(df):
    df = df[['county','state', 'num_uninsured']]
    df.drop_duplicates(inplace=True)
    return df['num_uninsured'].sum()
    
def get_table_values(df, df_demo, yesterday):
    pop = get_pop(df_demo)
    cases = get_cases(df, yesterday)
    deaths = get_deaths(df, yesterday)
    unemployment = get_unemployment(df)
    personal_income = get_personal_income(df, pop)
    pop_density = get_pop_density(df, pop)
    num_uninsured = get_num_uninsured(df)
    return pop, cases, deaths, unemployment, personal_income, \
        pop_density, num_uninsured
    

cd = '/Users/kianaocean/Documents/CMU/Python (95888)/Project/DFP-CCIP/'

csv_path = cd + 'data/county_level_merge.csv'
df = pd.read_csv(csv_path, thousands=',', dtype={'area_title': str, 'date_monthly': str, 'state_abbrv': str})
df['date_monthly'] = pd.to_datetime(df['date_monthly'])
df['date'] = pd.to_datetime(df['date'])

csv_path = cd + 'data/demographic_data.csv'
demo_df = pd.read_csv(csv_path)

# Set yesterday's date
yesterday = pd.to_datetime(date.today() - timedelta(days = 1))

# Get user input
county = input("Enter your county name: ").title()
state = input("Enter your state name: ").title()

if ((county == '') & (state == '')): # Entire US
    pop, cases, deaths, unemployment, personal_income, \
        pop_density, num_uninsured = get_table_values(df, demo_df, yesterday)
    print('Summary for the United States')
    
elif (county == ''): # Entire state
    state_df = df.loc[df['state'] == state]
    state_demo_df = demo_df.loc[demo_df['state'] == state]
    pop, cases, deaths, unemployment, personal_income, \
        pop_density, num_uninsured = get_table_values(state_df, state_demo_df, yesterday)
    print('Summary for the state of',state)
    
else: # County & state
    county_df = df.loc[(df['county'] == county) & (df['state'] == state)]
    county_demo_df = demo_df.loc[(demo_df['county'] == county) & (demo_df['state'] == state)]
    pop, cases, deaths, unemployment, personal_income, \
        pop_density, num_uninsured = get_table_values(county_df, county_demo_df, yesterday)
    print('Summary for',county,'County,',state)


# Print formatted table
output_dict = {}
output_dict['Total population:'] = pop
output_dict['Population density per square mile:'] = pop_density
output_dict['Number of people uninsured:'] = num_uninsured
output_dict['    percent uninsured:'] = (num_uninsured/pop)*100
output_dict['Unemployment rate last reported month:'] = unemployment
output_dict['Personal income per capita (2018):'] = personal_income
output_dict['New Covid-19 cases in last 14 days:'] = cases
output_dict['    per 100,000:'] = (cases/pop)*100000
output_dict['Covid-19 deaths in last 14 days:'] = deaths
for key, value in output_dict.items():
    if ((key == 'Unemployment rate last reported month:')|(key == '    per 100,000:')|(key == '    percent uninsured:')):
        print(f'{key:40}{value:.1f}')
    else:
        print(f'{key:40}{value:,.0f}')
output_df = pd.DataFrame.from_dict(output_dict, orient='index', columns=['Figure'])


