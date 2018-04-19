# -*- coding: utf-8 -*-
import crawlers
import csv
import re
import time


class Person:
    def __init__(self, name):
        self.name = name
        self._info = ''
    
    def set_name(self, name):
        self.name = name
    
    def set_phone(self, phone):
        self.phone = phone
    
    def set_info(self, info):
        self._info = info
    
    def get_info(self):
        return self._info
    
    def get_name(self):
        return self.name
    
    def get_phone(self):
        return self.phone

    def filter_phone(self):
        if not re.findall('\+[\d].+', self.phone):
            self.phone = ''
    

class TelegramContact:
    def __init__(self):
        self.telegram_url = "https://web.telegram.org/#/login"
        self.delimiter = ' '

    def save_contacts(self, persons, filename):
        with open(filename, 'w', newline='') as csvfile:
            contacts = csv.writer(csvfile)
            for row in persons:
                contacts.writerow([row.name, row._info])
        
    def get_contacts(self):
        crawler = crawlers.SeleniumCrawler()
        crawler.driver.get(self.telegram_url)
        i = 0
        db = []
        while True:
            print("Press any key to continue, 'e' to exit")
            key = input()
            if key == 'e':
                break
            persons = []
            try:
                contacts = crawler.driver.find_elements_by_xpath("//a[@class='md_modal_list_peer_name']")
                for contact in contacts:
                    contact.click()
                    time.sleep(1)
                    name = crawler.driver.find_elements_by_class_name('peer_modal_profile_name')[-1].text
                    info_elems = ''
                    try:
                        info_elems = crawler.driver.find_elements_by_xpath("//div[@class='md_modal_section_param_value']")
                        info_elems = [i.text for i in info_elems]
                    except Exception as ex:
                        print(ex)
                        pass
                    person = Person(name)
                    person.set_info(self.delimiter.join(info_elems))
                    persons.append(person)
                    crawler.driver.find_elements_by_class_name('md_modal_action_close')[-1].click()
            except Exception as ex:
                print(ex)
                pass
            
            try:
                self.save_contacts(persons, 'contactsx' + str(i) + '.csv')
            except Exception as ex:
                print(ex)
                pass
            i += 1
            db.append(persons)
        return db


tc = TelegramContact()
info = tc.get_contacts()
