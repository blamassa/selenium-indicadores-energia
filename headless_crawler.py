import re
import numpy as np


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

def boa_vista(mes, ano_index, ano):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(firefox_options = options)

    wait = WebDriverWait(driver, 15)

    print('Firefox headless aberto!')

    # Pagina do aplicativo
    #driver.get('http://www2.aneel.gov.br/aplicacoes_liferay/indicadores_de_qualidade/index.cfm')
    # Pagina do NO
    driver.get('http://www2.aneel.gov.br/aplicacoes_liferay/indicadores_de_qualidade/pesquisa.cfm?regiao=NO')

    element = driver.find_element_by_name('tipo')
    element.send_keys('Dados')

    element = driver.find_element_by_name('tipoE')
    element.send_keys('Concessionárias')

    time.sleep(1)
    element = driver.find_element_by_name('distribuidora')
    element.send_keys('CELPA')

    # print('periodo')
    time.sleep(1)
    # select = driver.find_element_by_name('periodo')
    # if mes in range(0,7)
    option = mes+2
    option = driver.find_element_by_xpath(f'/html/body/table/tbody/tr[3]/td[1]/select[4]/option[{option}]')
    option.click()

    # time.sleep(3)
    # select = Select(driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/td[1]/select[5]'))
    # all_options = [o.get_attribute('value') for o in select.options][:1]
    option = ano_index+2
    # wait.until(ec.presence_of_element_located((By.XPATH, f'/html/body/table/tbody/tr[3]/td[1]/select[5]/option[{option}]')))
    # print(f'Ano index + 1: {option}')
    if mes in range(0,7):
        option = ano_index+2
    else:
        option = ano_index+1
    option  = driver.find_element_by_xpath(f'/html/body/table/tbody/tr[3]/td[1]/select[5]/option[{option}]')
    option.click()

    driver.find_element_by_id('submit_obter_dados').click()
    driver.switch_to_window(driver.window_handles[1])
    # driver.close()

    time.sleep(2)
    table=driver.find_element_by_xpath("/html/body/div/table")
    # result_table = driver.find_element_by_xpath('/html/body/div/table')
    # print(driver.page_source)
    # driver.quit()
    return table,driver

def extract_info_BS(table):
    from bs4 import BeautifulSoup as BS
    content = table.get_attribute('innerHTML')#contents of that table
    soup = BS(content, 'html.parser')
    rows = [tr for tr in soup.findAll('tr')][4:]
    infos = [tr.findAll('td') for tr in rows]
# Printa os 20 primeiros caracteres
    return infos
#driver.quit()

def string_total(a):
    if len(a) > 1:
        string = ''
        for i in range(len(a)):
            string+=a[i]
        return string
    else:
        return a[0]

def save_to_file(infos, mes, ano):
    row = []
    for i in infos:
        line = []

        for el in i:
            b = str(el).replace('\xa0','')
            b = b[b.find('>')+1:]
            b = b[:b.find('<')-1]
            line.append(b)
        # print('UNIQUES')
        # print(np.unique(line))
        if '' in np.unique(line):
            continue

        # Mantendo somente alfabeto
        a = re.findall("[a-zA-Z]+", line[0])
        line[0] = string_total(a)

        line_str = ''
        for i in line:
            i = i.replace(',','.')
            line_str += i+', '
        row.append(line_str)

        f = open('celpa.csv', 'a')
        for r in row:
            f.write(f'\n,{ano},{mes},'+r)

        f.close()

################### EXECUTANDO ###################
ano_list = ['2019', '2018', '2017', '2016', '2015',
            '2014', '2013', '2012', '2011', '2010',
            '2009', '2008', '2007', '2006', '2005',
            '2004', '2003', '2002', '2001',# '2000'
            ]#[::-1]
indexes = list(range(len(ano_list)))[::-1]
for i in indexes:
    ano = ano_list[i]
    ano_index = i
    for mes in range(2,13):
        # mes = 12
        # ano = '2010'
        print(f'{ano}-{mes}')
        ### EXCEPTIONS
        # if ano in ['2000'] and mes in [1,2,3,4,5,6]:
        #     continue
        table, driver = boa_vista(mes = mes, ano_index = ano_index, ano = ano)
        infos = extract_info_BS(table)
        # print(infos)
        save_to_file(infos, mes,ano)
        print('SAVED!')
        driver.quit()
        # input('prosseguir?')
        print('OK\n\n')

    # input('presseguir?')
    break
