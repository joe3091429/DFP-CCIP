#!/usr/bin/python
# -*- coding: UTF-8 -*-

from dfp_ccip.ccip_utils.ccip_utils import CCIPUtils
from dfp_ccip.factory import load_local_data, scrapy_data
from dfp_ccip.validation import val_aspect, val_name


def main():
    print("Hi,")
    print("This is the entrance of the demo CCIP.")
    print("")

    print("Testing factory: ")
    load_local_data.get_data()
    scrapy_data.get_data()
    print("")

    print("Testing validation: ")
    val_aspect.val_aspect()
    val_name.val_name()
    print("")

    print("Testing CCIP utils: ")
    CCIPUtils.download_files()
    CCIPUtils.plot()
    CCIPUtils.map()

    print("I want to know you're running when I execute -m package")

if __name__ == "__main__":
    main()