import time
import csv
import traceback 

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException,NoSuchElementException
from bs4 import BeautifulSoup

from nuroa_model import NuroaModel

class NuroaScrapper:

    """const data"""
    URL = 'https://www.nuroa.com.mx/'
    DRIVER = '/home/edwin/Descargas/chromedriver' 
    CONTAINER_RESULTS_ID = 'nu_results_container' #ID
    ITEM_RESULT_CSS = 'nu_row' # CSS CLASS "FOR EVERY ITEM"
    ITEM_SEARCH_BOX_NAME = 's' # INPUT NAME 

    ITEM_NAME_ITEM_PROP = 'url' # ATTR ITEMPROP
    ITEM_DESCRIPTION_ITEM_PROP  = 'description' # ATTR ITEMPROP
    ITEM_PRICE_ITEM_PROP = 'price' # ATTR ITEMPROP
    ITEM_FEATURES_CSS = 'nu_features' # CSS CLASS
    ITEM_LOCATION_CSS = 'nu_sub' #ID
    ITEM_SPINNER_ID = 'nu_spinner_container' #ID
    ITEM_NEXT_LINK_ID = 'nu_page_forward' #ID

    def __init__(self):
        self.driver = None

    def initialize(self):
        self.driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
        self.driver.get(self.URL)
        time.sleep(1)
        
    def close_driver(self):
        self.driver.close()

    def search_filter(self, text_search):
        search_box = self.driver.find_element_by_name(self.ITEM_SEARCH_BOX_NAME)
        search_box.send_keys(text_search)
        search_box.submit()
        self.wait()

    def wait(self):
        elem = self.driver.find_element_by_tag_name("html")
        count = 0
        while True:
            count += 1
            if count > 20:
                print('Timing out after 10 seconds and returning')
                return
            time.sleep(.5)
            try:
                elem == self.driver.find_element_by_tag_name('html')
            except StaleElementReferenceException:
                return

    def download_data(self):
        self.data = set()
        
        try:  
            self.run_crawler()
        except Exception:
            traceback_str = str(traceback.format_exc())
            print('Error extract to data, message error:{0}'.format(traceback_str))
            return False
        else:
            print( 'Success finish, data extracted: {0}'.format(len(self.data)) )
            return True
    
    def run_crawler(self):

            self.wait()
            html = BeautifulSoup(self.driver.page_source, 'html.parser')
            items_results2 = html.find('div',id=self.CONTAINER_RESULTS_ID).find_all('div', {'class':self.ITEM_RESULT_CSS})

            for item in items_results2:
                item_temp_mapped = self.data_to_model(item)
                if item_temp_mapped is not None :
                    self.data.add(item_temp_mapped)
                else:
                    continue
            try:
                
                element_next_link  = self.driver.find_element_by_id(self.ITEM_NEXT_LINK_ID).find_element_by_tag_name('a')
                self.driver.execute_script("arguments[0].click();", element_next_link)
                WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located((By.ID, self.ITEM_SPINNER_ID)))
                self.run_crawler() #recursion

            except NoSuchElementException:
                return #finish recursion

    def data_to_model(self,selector_item):

        try:
            nuroa_model = NuroaModel()
            name = selector_item.find("a", {'itemprop':self.ITEM_NAME_ITEM_PROP})
            description = selector_item.find("div", {'itemprop':self.ITEM_DESCRIPTION_ITEM_PROP})
            price = selector_item.find("span", {'itemprop':self.ITEM_PRICE_ITEM_PROP})
            features = selector_item.find("ul", {'class':self.ITEM_FEATURES_CSS})
            location = selector_item.find("p", {'class':self.ITEM_LOCATION_CSS})
            nuroa_model.name = name.text.strip() if name else ''
            nuroa_model.description = description.text.strip() if description else ''
            nuroa_model.price = price.text.strip() if price else ''
            nuroa_model.features = features.text.strip() if features else ''
            nuroa_model.location = location.text.replace('Mapa','') if location else ''
            
        except Exception as error:
            print(f'Model mapping error, message error: {error}')
            return

        return nuroa_model

    def write_csv(self,path_save = None):
        with open('data_nuroa.csv', mode='w') as employee_file:

            data_writer = csv.writer(
                employee_file,
                delimiter=',',
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL
            )
            columns_names = [
                'Name',
                'Description',
                'Price',
                'Features',
                'Location'
            ]
            data_writer.writerow(columns_names)
                        
            for item in self.data:
                data_writer.writerow([
                    item.name,
                    item.description, 
                    item.price,
                    item.features,
                    item.location
                ])
