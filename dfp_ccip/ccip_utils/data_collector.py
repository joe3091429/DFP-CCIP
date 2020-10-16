'''
    File name: data_collector
    Group members: Kiana, Xiaoye, Joe
    Purpose: Collect data of health data from country, states, or counties
'''
import calendar
import datetime
import json
import re
import pandas as pd
import requests
from pandas import DataFrame


class DataCollector(object):
    
    def __init__(self):
        state_txt = './data/state.txt'
        csv_path = './data/county_level_merge.csv'
        state_popu = './data/demo_state.txt'
        self.country_url = 'https://api.covidtracking.com/v1/us/daily.json'
        self.states_url = 'https://api.covidtracking.com/v1/states/{}/daily.json'

        self.state2abbr, self.abbr2state = self.load_state_name(state_txt)
        self.csv_df = self.load_csv_df(csv_path)
        self.state2popu = self.load_state_popu(state_popu)

        self.show_state = None
        self.show_county = None

    def get_data(
            self, state: str, county: str, data_type: str,
            month: str, date: str) -> DataFrame:

        country_data, state_data = self.get_country_and_state_data(state, data_type=data_type)
        county_data = self.get_county_data(state=state, county=county)

        if month and date:
            start_date = '2020-{:0>2d}-{:0>2d}'.format(int(month), int(date))
            end_date = '2020-{:0>2d}-{:0>2d}'.format(int(month), int(date))
        elif month and not date:
            start_date = '2020-{:0>2d}-01'.format(int(month))
            end_date = '2020-{:0>2d}-{:0>2d}'.format(int(month), calendar.monthrange(int(2020), int(month))[1])
        elif not month and not date:
            start_date = '2020-02-01'
            end_date = '2020-10-31'

        all_data = self.integrate_data(
            country_data, state_data, county_data,
            data_type, start_date, end_date)

        return all_data

    def get_monthly_data(self, state: str, county: str, set_date_index: bool = True, last_day_needed: bool = False):
        df = DataFrame([])
        for i in range(2, 11):
            if last_day_needed:
                end_date = '2020-{:0>2d}-{:0>2d}'.format(int(i), calendar.monthrange(int(2020), int(i))[1])
                end_df = self.get_county_data(state, county, end_date, need_all_county=True)
                df = pd.concat([df, end_df], axis=0)
            date = '2020-{:0>2d}-01'.format(i)
            i_df = self.get_county_data(state, county, date, need_all_county=True)
            df = pd.concat([df, i_df], axis=0)
        if set_date_index:
            df = df.set_index('date')
            return df
        return df

    def get_covid19_data(
            self, state: str = None, county: str = None,
            start_date: str = '2020-02-01', end_date: str = '2020-09-01'
    ) -> DataFrame:
        """
        return a dataframe with date and cases in country, state, county level
        :param start_date: start_date: YYYY-MM-DD
        :param end_date: end_date: YYYY-MM-DD
        :param state: if not specific return only country
        :param county: if not specific return empty country and state
        """
        self.show_county = True if county else False
        self.show_state = True if state else False

        country_data, state_data = self.get_country_and_state_data(state)
        county_data = self.get_county_data(state=state, county=county)

        all_data = self.integrate_data(country_data, state_data, county_data, start_date, end_date)

        return all_data

    @staticmethod
    def integrate_data(
            country_data, state_data, county_data, data_type,
            start_str, end_str
    ) -> DataFrame:

        if data_type == 'infected':
            type1, type2 = 'positive', 'cases'
        else:
            type1, type2 = 'death', 'deaths'
        current_date = datetime.datetime.strptime(start_str, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_str, "%Y-%m-%d")
        if end_date > datetime.datetime.now():
            end_date = datetime.datetime.now() - datetime.timedelta(days=1)
            end_str = end_date.strftime('%Y-%m-%d')

        all_data = []  # date, country_count, state_count, county_count
        state_count = None
        while current_date <= end_date:
            date_str1 = current_date.strftime("%Y-%m-%d")
            date_str2 = current_date.strftime("%Y%m%d")
            if country_data is not None and country_data.size > 0:
                country_count = country_data[country_data['date'] == date_str2][type1].values
            if state_data is not None and state_data.size > 0:
                state_count = state_data[state_data['date'] == date_str2][type1].values
            county_count = county_data[county_data['date'] == date_str1][
                type2].values if county_data is not None else None

            if county_count is not None and state_count is not None and country_count is not None:
                all_data.append({
                    'country_count': int(country_count[0])
                    if country_count.size > 0 and country_count[0] != 'None' else 0,
                    'state_count': int(state_count[0])
                    if state_count.size > 0 and state_count[0] != 'None' else 0,
                    'county_count': int(county_count[0])
                    if county_count.size > 0 and county_count[0] != 'None' else 0,
                })
            elif state_count is not None and country_count is not None:
                all_data.append({
                    'country_count': int(country_count[0])
                    if country_count.size > 0 and country_count[0] != 'None' else 0,
                    'state_count': int(state_count[0])
                    if state_count.size > 0 and state_count[0] != 'None' else 0,
                })
            elif country_count is not None:
                all_data.append({
                    'country_count': int(country_count[0])
                    if country_count.size > 0 and country_count[0] != 'None' else 0,
                })

            current_date += datetime.timedelta(days=1)

        return DataFrame(all_data, index=pd.date_range(start_str, end_str))

    def get_country_and_state_data(self, state, data_type):
        """
        return state, country result
        type = infected or dead
        """

        result = requests.get(url=self.country_url)
        print('request country result ended')
        json_data = json.loads(result.text)
        country_data = self.convert_json_to_df(json_data, data_type)

        if len(state) > 2:
            state = self.state2abbr.get(state.lower(), '')

        if state:
            result = requests.get(url=self.states_url.format(state))
            print('request state result ended')
            json_data = json.loads(result.text)
            state_data = self.convert_json_to_df(json_data, data_type)
        else:
            state_data = None

        return country_data, state_data

    @staticmethod
    def convert_json_to_df(json_data, data_type) -> DataFrame:
        """
        convert the json format result from https://api.covidtracking.com to dataframe
        kept key: date, states, positive
        """
        data_type = 'positive' if data_type == 'infected' else 'death'
        kept_key = ['date', data_type]
        filtered_json = [
            dict([(key, str(data[key])) for key in kept_key])
            for data in json_data
        ]
        return DataFrame(filtered_json)

    def get_county_data(
            self, state: str, county: str, date: str = None, need_all_county: bool = False
    ) -> DataFrame:
        if len(state) == 2:
            state = self.abbr2state.get(state.upper(), '')
        elif len(state) > 2:
            abbr = self.state2abbr.get(state.lower(), '')
            state = self.abbr2state.get(abbr, '')

        county = self.normal_county_name(county)

        df = self.csv_df
        if date:
            df = df[df['date'] == date]
        if not county and not state:
            if need_all_county:
                return df
            else:
                return None  # DataFrame([])
        elif not county:
            return df[self.csv_df['state'] == state] if need_all_county else None
        else:
            return df[(self.csv_df['state'] == state) & (self.csv_df['county'] == county)]

    @staticmethod
    def normal_county_name(county):
        if not county:
            return ''
        tokens = county.split(' ')
        new_tokens = []
        for token in tokens:
            new_tokens.append(token[0].upper() + token[1:])
        return ' '.join(new_tokens)

    @staticmethod
    def load_state_name(txt_path: str):
        """
        map states name to their abbr
        """
        match_re = r'(.*) \((.*)\)'
        abbr2name = {}
        name2abbr = {}
        with open(txt_path) as f_in:
            for line in f_in:
                result = re.search(match_re, line.strip())
                fullname = result.group(1).split('/')
                abbr = result.group(2)
                for name in fullname:
                    name2abbr[name.lower()] = abbr
                    abbr2name[abbr] = name
        return name2abbr, abbr2name

    def load_state_popu(self, txt_path: str):
        """
        map states name to their population
        """
        name2popu = {}
        with open(txt_path) as f_in:
            for line in f_in.readlines()[1:-1]:
                tokens = line.strip().split('\t')
                name, popu = tokens[1], int(tokens[2].replace(',', ''))
                name2popu[name] = popu
                name2popu[name.lower()] = popu
                name2popu[self.state2abbr[name.lower()]] = popu
        name2popu['total'] = 321418820  # for whole country
        return name2popu

    @staticmethod
    def load_csv_df(csv_path: str) -> DataFrame:
        """
        load csv from url and return a dataframe
        """
        retry = 3
        df = None
        while retry:
            try:
                df = pd.read_csv(csv_path, dtype={"fips": str}, thousands=',')
                # print('csv loaded')
                break
            except TimeoutError as e:
                print('{}, retry: {}'.format(e, retry))
            finally:
                retry -= 1
        return df


if __name__ == '__main__':
    pass
    # dc = DataCollector()
    # data = dc.get_data('ca', 'Alameda', 'dead', '10', '9')
    # print(data)
    # data = dc.get_data('ca', 'Alameda', 'infected', '10', '9')
    # print(data)
    # dc.show(data)
