import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from nuroa_scrapper import NuroaScrapper


def main():
    nuroa = NuroaScrapper()
    nuroa.initialize()
    nuroa.search_filter('valladolid')
    nuroa.download_data()
    nuroa.write_csv()
    nuroa.close_driver()

if __name__=='__main__':
    print('Start...')
    main()
    print('End...')
