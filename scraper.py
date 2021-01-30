from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from collections import defaultdict
import pandas as pd
from selenium.webdriver.common.by import By


class Scraper:
    '''
    Class aimed to retrieve data directly from websites.
    '''
    def __init__(self, path, elements):
        '''
        args:
            -path: string, path to the website where de data is.

            -buttons: dict, buttons to be pressed in the website.
                      This dict has to have the following structure:
                      {
                          'name_of_the_button1': [button_type, xpath]
                      }
                      name_of_the_button: can be any, allows quick access to the 
                                          desired button
                      button_type: Currently only implemented "select" buttons
                      xpath: xpath of the button taken from the website
            
            -tables: dict, information about the table to be accesed.
                     This dict has to have the following structure:
                     {
                         'name_of_the_table': [number_of_columns, xpath]
                     }
                     name_of_the_table: can be any, allows quick access to the 
                                        desired table
                     number_of_columns: number of columns opf the table to be parsed
                     xpath: xpath of the button taken from the website

        '''
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(firefox_options=options)
        self.driver.get(path)
        self.elements = elements

        self.by_modes = {
            "id" : 'ID',
            "xpath" : 'XPATH',
            "link text" : 'LINK_TEXT',
            "partial link text" : 'PARTIAL_LINK_TEXT',
            "name" : 'NAME',
            "tag name" : 'TAG_NAME',
            "class name" : 'CLASS_NAME',
            "css selector" : 'CSS_SELECTOR'
        }

    def presh_button(self, name, button, value = None):
        '''
        Method for pressing any button in the website.

        args:
            -name: string, name of the button (key in buttons dict)
            -value: string, value to be selected
        '''
        if self.elements[name]['type'] == 'select':
            self.select_button(
                button = button,
                value = value
            )
        
        if self.elements[name]['type'] == 'click':
            self.click_button(button)

    def find_elements(self, name):
        '''
        '''
        elem_array = self.driver.find_elements(
                eval('By.' + self.by_modes[self.elements[name]['by'][0]]), 
                self.elements[name]['by'][1]
            )
        return elem_array

    def find_element(self, name):
        '''
        '''
        elem = self.driver.find_element(
                eval('By.' + self.by_modes[self.elements[name]['by'][0]]), 
                self.elements[name]['by'][1]
            )
        return elem

    def select_button(self, button, value):
        '''
        Specific method for select buttons.

        args:
            -xpath: string, xpath to the button
            -value: string, value to be selected
        '''
        name = Select(button)
        name.select_by_value(value)
    
    def click_button(button):
        '''
        '''
        button.click()


    def get_tdth_table(self, name):
        '''
        Retrieves data from a table as df.

        args:
            -name: string, name of the table
        '''
        table = self.find_element(name)

        data = [item.text for item in table.find_elements_by_xpath(
            ".//*[self::td or self::th]")]

        row = 0
        i = 0
        titles = []
        toret = defaultdict(list)
        for elem in data:
            if row == 0:
                titles.append(elem)
            else:
                toret[titles[i]].append(elem)

            i = i+1
            if i == (self.elements[name]['ncols']):
                i = 0
                row = row + 1

        return(pd.DataFrame(toret))

    def get_div_table(self, name):
        '''
        '''
        table = self.find_elements(name)
        toret = defaultdict(list)
        for elem in range(len(table)):
            colname = table[elem].find_element(
                eval('By.' + self.by_modes[self.elements[name]['by'][0]]), 
                self.elements[name]['colnames'][1]
                )
            unit = table[elem].find_elements(
                eval('By.' + self.by_modes[self.elements[name]['by'][0]]),
                self.elements[name]['rownames'][1]
                )
            for i in unit:
                toret[colname.text].append(i.text)
        return pd.DataFrame(toret)

    def close_client(self):
        '''
        Closes connection.
        '''
        self.driver.quit()


if __name__ == '__main__':