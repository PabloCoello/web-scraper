from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from collections import defaultdict
import pandas as pd


class Scraper:
    '''
    Class aimed to retrieve data directly from websites.
    '''
    def __init__(self, path, buttons, tables):
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
        self.buttons = buttons
        self.tables = tables

    def presh_button(self, name, value):
        '''
        Method for pressing any button in the website.

        args:
            -name: string, name of the button (key in buttons dict)
            -value: string, value to be selected
        '''
        if self.buttons[name][0] == 'select':
            self.select_button(
                xpath = self.buttons[name][1],
                value = value
            )

    def select_button(self, xpath, value):
        '''
        Specific method for select buttons.

        args:
            -xpath: string, xpath to the button
            -value: string, value to be selected
        '''
        name = Select(self.driver.find_element_by_xpath(xpath))
        name.select_by_value(value)

    def get_table(self, name):
        '''
        Retrieves data from a table as df.

        args:
            -name: string, name of the table
        '''
        table = self.driver.find_element_by_xpath(self.tables[name][1])

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
            if i == (self.tables[name][0]):
                i = 0
                row = row + 1

        return(pd.DataFrame(toret))

    def close_client(self):
        '''
        Closes connection.
        '''
        self.driver.quit()


if __name__ == '__main__':
    # Example 1:

    path = 'http://www.intecmar.gal/Informacion/biotoxinas/Evolucion/CierresBatea.aspx'
    buttons = {
        'toxicidade': ['select','//*[@id="ctl00_Contenido_dpToxina2"]'],
        'year': ['select', '//*[@id="ctl00_Contenido_dpAno2"]']
    }

    tables = {
        'main': [14, '//*[@id="ctl00_Contenido_GridView2"]']
    }
    sc = Scraper(path, buttons, tables)

    sc.presh_button(
        name = 'toxicidade',
        value='Todas'
    )
    for year in range(1996, 2022):
        sc.presh_button(
            name = 'year',
            value = str(year)
        )
        df = sc.get_table(name='main')
        df.to_excel('total_'+str(year)+'.xlsx')
            
    sc.close_client()