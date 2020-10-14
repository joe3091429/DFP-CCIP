#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 15:52:49 2020

@author: kianaocean
"""

from urllib.request import urlopen
import json
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.figure_factory as ff
from plotly.offline import plot

# Creates charts and maps of unemployment numbers if user asks for economic data

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

cd = '/Users/kianaocean/Documents/CMU/Python (95888)/Project/DFP-CCIP/'

# Import base county level map
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# Import latest unemployment data CSV & do cleaning
csv_path = cd + 'data/unemployment.csv'
df = pd.read_csv(csv_path, dtype={'fips': str, 'area_title': str, 'civ_labor_force': str, \
                                  'employed': str, 'unemployed': str, 'unemployed_rate': str, 'date_monthly': str})
df = clean_fips(df)
df = df.loc[df['unemployed_rate'] != '-'] # filter out any missing rates
df['unemployed_rate'] = pd.to_numeric(df['unemployed_rate'])
df['civ_labor_force'] = df['civ_labor_force'].str.replace(',', '').astype(float)
df['unemployed'] = df['unemployed'].str.replace(',', '').astype(float)
df = df.loc[df['fips'] != '00nan'] # filter out any missing counties


# Get user input
state = input("Enter your state name: ").title()
if (state != ''):
    county = input("Enter your county name: ").title()
else:
    county = ''
date_input = input("Enter month (MM/YYYY) in last 14 months: ")


# Filters df to relevant month of input received from user
    # Sets date to min or max if date provided is out of range
df['date_monthly'] = pd.to_datetime(df['date_monthly'])
max_date = df['date_monthly'].max()
min_date = df['date_monthly'].min()
if (date_input != ''):
    date = datetime.strptime(date_input, '%m/%Y')
    if (pd.to_datetime(date) > max_date):
        date = max_date
    elif (pd.to_datetime(date) < min_date):
        date = min_date
    df = df.loc[(df['month'] == date.month) & (df['year'] == date.year)]

# Limit to relevant data
df = df[['state','county','fips','unemployed_rate','date_monthly','civ_labor_force','unemployed']]
df.drop_duplicates(inplace=True)


# Create maps & plots - outputs one figure depending on user input
if ((state == '') & (county == '') & (date_input == '')):
    make_line_graph(df, 'United States')
elif ((state != '') & (county == '') & (date_input == '')):
    state_df = df.loc[df['state'] == state]
    make_line_graph(state_df, state)
elif ((state != '') & (county != '') & (date_input == '')):
    statecounty_df = df.loc[(df['state'] == state) & (df['county'] == county)]
    area = county + ' County, ' + state
    make_line_graph(statecounty_df, area)
elif ((state == '') & (county == '') & (date_input != '')):
    date_str = date.strftime('%B %Y')
    title = 'US Unemployment Rates by County, ' + date_str
    fig = px.choropleth(df, geojson=counties, locations='fips', color='unemployed_rate', hover_name='county', title=title,\
                    color_continuous_scale='Blues', scope='usa', labels={'unemployed_rate':'Unemployment Rate'})
    plot(fig)
else:
    state_df = df.loc[df['state'] == state]
    date_str = date.strftime('%B %Y')
    title = state + ' Unemployment Rates by County, ' + date_str
    fig = ff.create_choropleth(fips=state_df['fips'], values=state_df['unemployed_rate'], scope=[state], \
                               show_state_data=True, round_legend_values=True, legend_title='Unemployment Rate', \
                                       county_outline={'color': 'rgb(255,255,255)', 'width': 0.5},exponent_format=True, show_hover=True, title=title)
    plot(fig)
