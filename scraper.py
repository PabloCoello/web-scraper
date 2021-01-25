from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from collections import defaultdict
import pandas as pd


class Scraper:
    '''
    '''
    def __init__(self, path, buttons, tables):
        '''
        '''
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(firefox_options=options)
        self.driver.get(path)
        self.buttons = buttons
        self.tables = tables

    def presh_button(self, name, value):
        '''
        '''
        if self.buttons[name][0] == 'select':
            self.select_button(
                xpath = self.buttons[name][1],
                value = value
            )

    def select_button(self, xpath, value):
        '''
        '''
        name = Select(self.driver.find_element_by_xpath(xpath))
        name.select_by_value(value)

    def get_table(self, name):
        '''
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
        '''
        self.driver.quit()


if __name__ == '__main__':
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