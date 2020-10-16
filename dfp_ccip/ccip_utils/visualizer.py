"""
This class is used to respond to user's choice.(health data, health_economy data, health_demographic data)
All the visualization will be done in this class.
Possible usage of this class is listed under (if __name__ == '__main__':)
"""
import calendar
import datetime
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
from typing import List
from urllib.request import urlopen
from pandas import DataFrame
from dfp_ccip.ccip_utils.data_collector import DataCollector
from dfp_ccip.ccip_utils.ccip_utils import CCIPUtils


class Visualizer(object):
    """
    menu class
    """

    def __init__(self, output: str = None):
        # self.output = output if output else r'output'
        self.data_collector = DataCollector()

    def health_data(self, state: str, county: str):
        """
        If no state and no county, country level query.
        If state and no county, state level query.
        If state and county, county level query.
        :param state: target state
        :param county: target county
        """
        while True:
            input_result = self.get_input()
            print("Processing data, please wait...")
            month, date = input_result  # convert input into month and date

            if month and date:  # specifiv day
                if county and state:
                    # all month, date, county and state are valid
                    # show data on exact date (country, state, county)
                    self.show_on_bar(state=state, county=county, month=month, date=date, data_type='infected')
                elif state:
                    # draw map on state(state level)
                    self.show_on_map(state=state, county=county, month=month, date=date, data_type='infected')
                else:
                    # draw map on state(country level)
                    self.show_on_map(state=state, county=county, month=month, date=date, data_type='infected')

            elif month and not date:  # specific month
                if county and state:
                    # show monthly data (country, state, county)
                    self.show_on_line(state=state, county=county, month=month, date=date, data_type='infected')
                    self.show_on_line(state=state, county=county, month=month, date=date, data_type='dead')
                elif state:
                    # show monthly data (country, state)
                    self.show_on_line(state=state, county=county, month=month, date=date, data_type='infected')
                    self.show_on_line(state=state, county=county, month=month, date=date, data_type='dead')
                else:
                    # show monthly data (country)
                    self.show_on_line(state=state, county=county, month=month, date=date, data_type='infected')
                    self.show_on_line(state=state, county=county, month=month, date=date, data_type='dead')

            elif not month and not date:  # from Feb 1st to now
                if county and state:
                    # show data till now (country, state, county)
                    self.show_on_line(state=state, county=county, month=month, date=date, data_type='infected')
                    self.show_on_line(state=state, county=county, month=month, date=date, data_type='dead')
                elif state:
                    # show data till now (country, state)
                    self.show_on_line(state=state, county=county, month=month, date=date, data_type='infected')
                    self.show_on_line(state=state, county=county, month=month, date=date, data_type='dead')
                else:
                    # show data till now (country)
                    self.show_on_line(state=state, county=county, month=month, date=date, data_type='infected')
                    self.show_on_line(state=state, county=county, month=month, date=date, data_type='dead')

            else:
                print('illegal input')
                continue

            # ask
            while True:
                exit_flag = input('1. continue\n2. exit\n')
                if exit_flag.strip() in ['1', '2']:
                    break
                else:
                    print('enter 1 or 2')

            if exit_flag.strip() == '2':  # exit searching
                break

    def health_eco_data(self, state: str, county: str):
        '''
        If no state and no county, country level query.
        If state and no county, state level query.
        If state and county, county level query.
        This functions shows health data and economy related data.
        :param state: target state
        :param county: target county
        '''
        print("Processing data, please wait...")
        if state and county:  # left_y: cumulative positive cases, right_y: monthly unemployment rate
            self.draw_on_line_with_double_y(
                state=state, county=county,
                col1='cases', col2='unemployed_rate',
                x_name='date', y1_name='number of cases', y2_name='%', max_percent=100,
                left_auto=True, right_auto=False
            )
        elif state:  # left_y:  positive cases per 100,000, right_y: monthly unemployment rate
            self.draw_on_line_with_double_y(
                state=state, county=county,
                col1='infection_rate', col2='unemployment_rate',
                x_name='date', y1_name='positive cases per 100,000', y2_name='%', max_percent=20,
                left_auto=True, right_auto=True
            )
        else: # left_y:  positive cases per 100,000, right_y: monthly unemployment rate
            self.draw_on_line_with_double_y(
                state=state, county=county,
                col1='infection_rate', col2='unemployment_rate',
                x_name='date', y1_name='positive cases per 100,000', y2_name='%', max_percent=20,
                left_auto=True, right_auto=True
            )

    def health_demo_data(self, state: str, county: str):
        '''
        If no state and no county, country level query.
        If state and no county, state level query.
        If state and county, county level query.
        This functions shows health data and demographic related data.
        :param state: target state
        :param county: target county
        '''
        print("Processing data, please wait...")
        if county:  # target county's data until now
            county_data = self.data_collector.get_county_data(state=state, county=county, need_all_county=True)
        else:  # county's data with in the state, if state is '', then retrieve whole country's data
            date = '2020-08-01'  # set to 2020-08-01 because demo data for sep and oct is unavailable
            county_data = self.data_collector.get_county_data(state, county, date, need_all_county=True)

        # select cases and total_population and # filter those total_population = NaN
        county_data = county_data[['date', 'cases', 'total_population', 'fips']].dropna().set_index('date')
        positive_rate = county_data['cases'] / county_data['total_population']
        positive_percent = DataFrame(positive_rate.mul(100))
        positive_percent.columns = ['positive_percent']

        if state and county:  # line chart, y axis means infection rate(positive cases / county population)
            self.draw_positive_line(positive_percent)
            # save_name = 'positive-percent-data-{}-{}.csv'.format(state, county)
            self.save(county_data, "")
        else:  # Map, show infection rate for different counties with in state/country
            map_data = pd.concat([county_data, positive_percent], axis=1)
            # print(map_data)
            self.draw_a_map(map_data, 'positive_percent', 'positive percent', [0, 1])
            self.save(map_data, "")

    @staticmethod
    def draw_positive_line(df: DataFrame):
        # helper function
        fig, axis = plt.subplots(figsize=(12, 8))
        df.plot(ax=axis)
        axis.set_xlabel('date')
        axis.set_ylabel('%')
        plt.legend(['positive percent'], loc='upper left')
        plt.show()

    def draw_on_line_with_double_y(
            self,
            state: str, county: str,
            col1: str, col2: str,
            x_name: str, y1_name: str, y2_name: str,
            max_percent: int, left_auto: bool, right_auto: bool
    ):
        """
        draw a line figure with 2 y-axis
        """
        df = self.data_collector.get_monthly_data(state, county, set_date_index=False, last_day_needed=True)

        df = self.deal_with_state_and_country(df, state, county)

        fig, left_axis = plt.subplots(figsize=(12, 8))

        l1, = left_axis.plot(df[[col1]], color='r')
        right_axis = left_axis.twinx()
        l2, = right_axis.plot(df[[col2]], color='b')

        if not left_auto:
            left_axis.set_ylim(0, max_percent)
            left_axis.set_yticks(np.arange(0, max_percent, 20))

        # set range, precision
        if not right_auto:
            right_axis.set_ylim(0, max_percent)
            right_axis.set_yticks(np.arange(0, max_percent, 20))

        # set title, label, color
        left_axis.set_xlabel(x_name)
        left_axis.set_ylabel(y1_name)
        left_axis.tick_params(axis='y')
        right_axis.set_ylabel(y2_name)
        right_axis.tick_params(axis='y')

        left_axis.set_title('monthly positive cases line & unemployment rate line')

        plt.legend([l1, l2], [col1, col2], loc='upper left')
        plt.show()

        # save_name = 'health-eco-data-{}-{}.csv'.format(state, county)
        self.save(df, '')

    def deal_with_state_and_country(self, df: DataCollector, state: str, county: str):
        # helper function used to handle no state, no county situation
        if state and county:
            df = df.set_index('date')
            return df
        else:
            # calculate state/country level unemployment rate and positive cases per 100,000
            new_df = DataFrame([], columns=['date', 'infection_rate', 'unemployment_rate', 'cases', 'popu'])
            new_end_df = DataFrame([], columns=['date', 'infection_rate', 'unemployment_rate', 'cases', 'popu'])
            for i in range(2, 11):
                end_date = '2020-{:0>2d}-{:0>2d}'.format(int(i), calendar.monthrange(int(2020), int(i))[1])

                # print(end_date)
                end_df = df[df['date'] == end_date]
                sum_end_cases = end_df['cases'].astype(float).sum()
                # print(end_df)

                date = '2020-{:0>2d}-01'.format(i)
                # print(date)
                i_df = df[df['date'] == date]  # first day of every
                # print(i_df)
                # i_df = i_df
                sum_cases = sum_end_cases - i_df['cases'].astype(float).sum()
                sum_unemploy = i_df['unemployed'].astype(float).sum()
                sum_labor = i_df['civ_labor_force'].astype(float).sum()
                sum_popu = self.data_collector.state2popu[state] if state else self.data_collector.state2popu['total']
                new_row = DataFrame(
                    [[date, sum_cases / sum_popu * 100000, sum_unemploy / sum_labor * 100, sum_cases, sum_popu]],
                    columns=['date', 'infection_rate', 'unemployment_rate', 'cases', 'popu'])
                new_df = pd.concat([new_df, new_row], axis=0)

            # print(new_df)
            new_df = new_df.set_index('date').dropna()
            return new_df

    @staticmethod
    def get_input():
        print("Please input search month and date. Available since Feb 1st .")
        print("You can choose to specify month only or month and date")
        print("If you don't want to set any dates, please press enter")

        input_result = input('Input format: (eg. 3 2, means Mar 2nd, separated by space)\n')
        if input_result:
            tokens = input_result.strip().split(' ')
            if len(tokens) == 1:
                if tokens[0].isdigit() and (1 < int(tokens[0]) < 11):
                    return tokens[0], ''
                else:
                    print("Wrong input, will show default data")
            else:
                if tokens[0].isdigit() and (1 < int(tokens[0]) < 11):
                    weekDay, monthCountDay = calendar.monthrange(2020, int(tokens[0]))
                    # print("this month have days: ",datetime.date(2020,int(tokens[0]), day=monthCountDay).day)
                    if 0 < int(tokens[1]) <= int(datetime.date(2020, int(tokens[0]), day=monthCountDay).day):
                        return tokens[0], tokens[1]
                print("Wrong input, will show default data")
        return '', ''

    def show_on_map(self, state: str, county: str, month: str, date: str, data_type: str):
        date = '2020-{:0>2d}-{:0>2d}'.format(int(month), int(date))
        county_data = self.data_collector.get_county_data(state, county, date, need_all_county=True)
        self.draw_a_map(county_data, 'cases', 'positive cases', [0, 4000])
        save_name = ''
        self.save(county_data, save_name)

    @staticmethod
    def draw_a_map(df: DataFrame, col_name: str, label_name: str, data_range: List[int]):
        with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
            counties = json.load(response)
        fig = px.choropleth_mapbox(
            df, geojson=counties, locations='fips', color=col_name,
            color_continuous_scale="OrRd",
            mapbox_style="carto-positron",
            range_color=(data_range[0], data_range[1]),
            zoom=3, center={"lat": 37.0902, "lon": -95.7129},
            opacity=0.5,
            labels={col_name: label_name})
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.show()

    def show_on_bar(self, state: str, county: str, month: str, date: str, data_type: str):
        """
        use bar to show data
        """
        df = self.data_collector.get_data(state=state, county=county, data_type=data_type, month=month, date=date)
        df.plot(kind='bar', figsize=(10, 6))
        plt.xticks([])
        plt.show()

        save_name = '{}-{}-{}-{}-{}.csv'.format(state, county, month, date, data_type)
        self.save(df, save_name)

    def show_on_line(self, state: str, county: str, month: str, date: str, data_type: str):
        """
        use line to draw data
        """
        # df = self.data_collector.get_data(state=state, county=county, data_type=data_type, month=month, date=date)
        df = self.data_collector.get_data(state=state, county=county, data_type=data_type, month=month, date=date)
        df = df - df.shift(1)
        df = df.dropna().drop([df.index[-1]])

        if county:
            self.line_with_subplot(df, data_type)
        else:
            self.line_without_subplot(df, data_type)

        save_name = '{}-{}-{}-{}-{}.csv'.format(state, county, month, date, data_type)
        self.save(df, save_name)

    @staticmethod
    def line_with_subplot(df: DataFrame, data_type: str):
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(25, 8))

        l1, = axes[0].plot(df.country_count, label='country')
        l1, = axes[0].plot(df.state_count, label='state')
        axes[0].legend(loc='upper left')

        l2, = axes[1].plot(df.state_count, label='state')
        l2, = axes[1].plot(df.county_count, label='county')
        axes[1].legend(loc='upper left')

        axes[1].set_title('Incremental {} cases in state and county'.format(data_type))
        axes[0].set_title('Incremental {} cases in country and state'.format(data_type))

        plt.show()

    @staticmethod
    def line_without_subplot(df: DataFrame, data_type: str):
        df.plot(kind='line', title='Incremental {} cases in country and/or state'.format(data_type))
        plt.legend()
        plt.show()

    def save(self, df: DataFrame, save_name: str):
        CCIPUtils.download_files(df)
        # input_result = input('save? (y/n)\n')
        # if input_result.strip() == 'y':
        #     df.to_csv(os.path.join(self.output, save_name))


if __name__ == '__main__':
    pass
    # print("test")
    # vi = Visualizer()
    # Health only
    # vi.health_data('', '')  # country level
    # 1. month & date: Map of positive cases in the whole country at the specific date
    # 2. month: Line of incremental positive/death cases in the whole country within the whole month
    # 3. no month no date: line of incremental death/positive case from the beginning of the pandemic

    # vi.health_data('california', '')  # state level
    # 1. month & date: Map of positive cases in the whole state at the specific date
    # 2. month: Line of incremental positive/death cases in the whole state within the whole month
    # 3. no month no date: line of incremental death/positive case from the beginning of the pandemic

    # vi.health_data('california', 'alameda')  # county level
    # 1. month & date: bar chart for positive cases in county, state, country
    # 2. month: Line of incremental positive/death cases in the whole state within the whole month
    # 3. no month no date: line of death case, line of positive case from the beginning of the pandemic

    #
    # # Health & Eco
    # vi.health_eco_data('california', '')  # country level: monthly infection rate line & unemployment rate line
    # vi.health_eco_data('california', '')  # state level: monthly infection rate line & unemployment rate line
    # vi.health_eco_data('california', 'alameda')  # county level: monthly infection cases & unemployment rate line
    #
    # # Health & Demo

    # vi.health_demo_data('', '')  # country level Map of infection rate.
    # vi.health_demo_data('california', '')  # state level Map of infection rate.
    # vi.health_demo_data('california', 'alameda')  # county level: infection rate line for different days
