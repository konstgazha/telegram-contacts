from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SeleniumCrawler:
    def __init__(self):
        self.wait_n_seconds = 5
        self.driver = webdriver.Chrome()

    def parse_elems_by_class(self, class_name):
        return self.driver.find_elements_by_class_name(class_name)
    
    def parse_elems_by_xpath(self, xpath):
        return self.driver.find_elements(By.XPATH, xpath)

    def wait_loading_by_class(self, class_name):
        try:
            WebDriverWait(self.driver, self.wait_n_seconds).until(
                EC.presence_of_element_located((By.CLASS_NAME , class_name))
            )
            return True
        except:
            return False
    
    @staticmethod
    def get_hrefs_from_soup_by_tag(soup, tag, attr_name, attr_value):
        return [tag['href'] for tag in 
                soup.find_all(tag, attrs={attr_name: attr_value, 'href': True})]

    def close(self):
        self.driver.quit()
    
    def get_soup(self, url):
        self.driver.get(url)
        source = self.driver.page_source
        return BeautifulSoup(source, 'html5lib')
