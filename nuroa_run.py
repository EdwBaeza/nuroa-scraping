import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from nuroa_scrapper import NuroaScrapper


def main():
    nuroa = NuroaScrapper()
    nuroa.initDriver()
    nuroa.searchFilter('valladolid')
    nuroa.downloadData()
    nuroa.writeCSV()
    nuroa.closeDriver()

if __name__=='__main__':
    print('Start...')
    main()
    print('End...')
