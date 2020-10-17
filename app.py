#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
    File name: app
    Group members: Kiana, Xiaoye, Joe
    Purpose: the main program of Covid Community Impact Platform
'''

import sys, time
from dfp_ccip.ccip_utils.ccip_utils import CCIPUtils
from dfp_ccip.ccip_utils import create_sum_tb
from dfp_ccip.factory import merge_countylevel
from dfp_ccip.validation import val_aspect, val_name, val_map_tb
from dfp_ccip.ccip_utils.unemployment_figs import UnemploymentFigs
from dfp_ccip.ccip_utils.visualizer import Visualizer

def main():

    print("\nHi, welcome to Covid-19 Community Impact Platform, in here you can explore different aspects and impacts with Covid-19.\n")

    # Select the way to input data
    print('Choose a way to input data:')
    print('1) Existed files (We will RECOMMEND you to choose this option for faster loading)\n2) Scraping \nQ) Explore next time\n')
    option = input('Your choice: ').strip()

    # Keep a dataframe for main code
    if option == '1':
        print('\nLoading data... \n')
    elif option == '2':
        print('\nStart scraping data... \n')
        start_time = time.time()
        merge_countylevel.MergeCountyLevel.start()
        print('--- Successfully scraping data in %d seconds ---\n' % (time.time() - start_time))
    elif option == 'q' or option == 'Q':
        print("\nLook forward to seeing you.")
        sys.exit()
    else:
        print("\nIt's not a valid option.")
        sys.exit()

    # Input the level of area
    explore = ''
    val_map_tb.val_map_tb()
    
    while(explore != 'Q'):
        val_result = False 
        while(val_result != True):
            state, county = '',''
            print('Choose the level of area (default as country-level):\n1) County\n2) State\n3) Country\n')
            area_level = input('Your choice of level: ').strip()

            if area_level == '1':
                print('The state of the county you want to explore \n')
                state = input('State: ').strip()
                print('The county you want to explore \n')
                county = input('County: ').strip()
                print("\n" + "State: " + state + " County: " + county + "  Searching......" )
                
            elif area_level == '2':
                print('The state you want to explore \n')
                state = input('State: ').strip()
                print("\n" + "State: " + state + "  Searching......")
                
            else:
                print("\nCountry: US  Searching......\n")
            
            # validate the name
            state, county, val_result = val_name.val_name(state, county, val_result)
            if val_result == False:
                print('\n================= The validation fails, please type correct region name =================\n')
            else:
                print('\n================= The validation passes =================\n')

        # show summary table
        title_state = state.title()
        title_county = county.title()
        sum_table = create_sum_tb.CreateSumTable(title_state, title_county)

        # Download or not
        print('\nWould you like to download this table? (Default as No)\nY) Yes, download it and keep explore\nN) No, just move on\n')
        load_option = input('Download: ').strip()
        print('')
        if load_option == 'Y' or load_option == 'y':
            CCIPUtils.download_files(sum_table)
        else:
            print('keep explore...\n')

        # input aspect and check the options
        validate_aspect = False
        while(validate_aspect != True):
            print('Choose aspects you want to explore:\n1) Health\n2) Economy\n3) Health + Demographic\n4) Health + Economy\n')
            aspect = input('Your choice of level: ').strip()
            print('')
            validate_aspect = val_aspect.val_aspect(aspect)
        
        # show visualization
        if aspect == '1':
            vi = Visualizer()
            vi.health_data(state, county)
        elif aspect == '2':
            df = UnemploymentFigs.create_economy_data(title_state, title_county)
        elif aspect == '3':
            vi = Visualizer()
            vi.health_demo_data(state, county)
        elif aspect == '4':
            vi = Visualizer()
            vi.health_eco_data(state, county)

        # continue or quit
        print('\nFind more explorations? (Default as No)\nY) Yes, keep explore new findings\nN) No, just quit')
        explore_opt = input('Option: ').strip()
        print('')
        if explore_opt == 'Y' or explore_opt == 'y':
            explore = ''
        else: 
            explore = 'Q'
        

if __name__ == "__main__":
    main()