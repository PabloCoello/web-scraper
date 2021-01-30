# Example 1:
elements = {
    'toxicidade': {
        'type': 'select',
        'by': ('xpath', '//*[@id="ctl00_Contenido_dpToxina2"]')
    },
    'year':{
        'type': 'select',
        'by': ('xpath', '//*[@id="ctl00_Contenido_dpAno2"]')
    },
    'main':{
        'type': 'tdth_table',
        'by': ('xpath', '//*[@id="ctl00_Contenido_GridView2"]'),
        'ncols': 14
    }
}

path = 'http://www.intecmar.gal/Informacion/biotoxinas/Evolucion/CierresBatea.aspx'
sc = Scraper(path, elements)

sc.presh_button(
    name = 'toxicidade',
    button = sc.find_element('toxicidade'),
    value='Todas'
)
for year in range(1996, 2022):
    sc.presh_button(
        name = 'year',
        button = sc.find_element('year'),
        value = str(year)
    )
    df = sc.get_tdth_table(name='main')
    df.to_excel('total_'+str(year)+'.xlsx')
        
sc.close_client()