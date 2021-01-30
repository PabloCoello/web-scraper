    # Example 2:
    # https://selenium-python.readthedocs.io/locating-elements.html

    elements = {
        'dial': {
            'by': ('class name', 'c1.c2')
        },
        'table':{
            'type': 'div_table',
            'by': ('class name', 'a5.d32'),
            'colnames':('class name', 'd34'),
            'rownames':('class name', 'd36')
        }
    }

    months = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 
              'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    toret = defaultdict(list)
    years = [2016, 2017, 2018, 2019, 2020]
    letters = ['A','B','C','E','F','G','I','L','M','N','O','P','R','S','T','V']
    for month in months:

        #####################
        path = 'https://seatemperature.info/es/{}/galicia-temperatura-del-agua-del-mar.html'.format(month)
        sc = Scraper(path, elements)


        ###############################
        dial = sc.find_elements('dial')
        for button in range(len(dial)):
            dial.clear()
            dial = sc.find_elements('dial')
            tag = dial[button].find_element(By.CLASS_NAME , 'c4').get_attribute('value')
            if tag in letters:
                dial[button].click()
                ###############################
                df = sc.get_div_table('table')

        sc.close_client()

    df = pd.DataFrame(toret)
    df.to_excel('temperatura.xlsx')
