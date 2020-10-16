#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
    File name: merge_countylevel
    Group members: Kiana, Xiaoye, Joe
    Purpose: Merges Personal Income, Unemployment, Demographic, and Covid data
'''
from dfp_ccip.factory import scrape_personal_income as pi
from dfp_ccip.factory import scrape_unemployment as ue
from dfp_ccip.factory import scrape_demo_social as dm
import pandas as pd
from datetime import datetime

class MergeCountyLevel():

    def start():
        try:
            def clean_fips(df):
                df.rename(columns = {'fips':'fips_old'}, inplace = True)
                num_rows, num_cols = df.shape
                fips_list = []
                for i in range(num_rows):
                    fips_clean = str(df.iloc[i]['fips_old']).zfill(5)
                    fips_list.append(fips_clean)
                df['fips'] = fips_list
                return df

            # Merges Personal Income, Unemployment, Demographic, and Covid data

            # Personal income
            pi_df = pi.get_pi_df()
            # Rename columns in personal income data
            pi_df.rename(columns = {'GeoFips':'fips', 'DataValue':'personal_income'}, inplace = True)
            # Only keep required columns
            pi_df = pi_df[['fips', 'personal_income']]

            # Unemployment
            ue_df = ue.get_ue_df()
            ue_df.drop(columns=['area_code','state_fips', 'county_fips', 'period', 'state', 'county'], inplace=True)

            # Demographics
            dm.ScrapeDS()
            csv_path = 'data/demographic_data.csv'
            de_df = pd.read_csv(csv_path)
            de_df = clean_fips(de_df)
            de_df.drop(columns=['fips_old', 'state','county','num_unemployed_CHR','labor_force', \
                                'percent_unemployed_CHR','num_unemployed_CDC','percent_unemployed_CDC',\
                                    'percentile_rank_unemployed'], inplace=True)

            # Covid
            csv_url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
            co_df = pd.read_csv(csv_url, dtype={"fips": str})

            # Create month/year columns for Covid data
            num_rows, num_cols = co_df.shape
            month_list = []
            year_list = []
            for i in range(num_rows):
                date = datetime.strptime(co_df.iloc[i]['date'], '%Y-%m-%d')
                month = date.month
                year = date.year
                month_list.append(month)
                year_list.append(year)
            
            co_df['month'] = month_list
            co_df['year'] = year_list

            # Merge data
            merge1 = pd.merge(co_df, ue_df, how='left', on=['fips','month','year'])
            merge2 = pd.merge(merge1, pi_df, how='left', on='fips')
            merge_final = pd.merge(merge2, de_df, how='left', on=['fips'])

            # Export to csv
            merge_final.to_csv ('data/county_level_merge.csv', index=None)
        except Exception:
            raise

