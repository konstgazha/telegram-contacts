# -*- coding: utf-8 -*-
import crawlers


class Person:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
    
    def set_name(self, name):
        self.name = name
    
    def set_phone(self, phone):
        self.phone = phone
    
    def get_name(self):
        return self.name
    
    def get_phone(self):
        return self.phone


class TelegramContact:
    def __init__(self):
        self.telegram_url = "https://web.telegram.org/#/login"

    def get_contacts(self):
        crawler = crawlers.SeleniumCrawler()
        crawler.driver.get(self.telegram_url)
        print("Press any key to continue")
        input()
        
        persons = []
        contacts = crawler.driver.find_elements_by_xpath("//a[@class='md_modal_list_peer_name']")
        for contact in contacts:
            contact.click()
            name = crawler.driver.find_elements_by_class_name('peer_modal_profile_name')[-1].text
            phone = crawler.driver.find_elements_by_class_name('peer_modal_profile_name')[0].text
            persons.append(Person(name, phone))
            crawler.driver.find_elements_by_class_name('md_modal_action_close')[-1].click()
            
        return persons


tc = TelegramContact()
info = tc.get_contacts()