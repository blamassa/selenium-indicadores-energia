from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

options = Options()
#options.add_argument('--headless')
driver = webdriver.Firefox(firefox_options = options)
print('Firefox headless aberto!')

# Pagina do aplicativo
#driver.get('http://www2.aneel.gov.br/aplicacoes_liferay/indicadores_de_qualidade/index.cfm')
# Pagina do NO
driver.get('http://www2.aneel.gov.br/aplicacoes_liferay/indicadores_de_qualidade/pesquisa.cfm?regiao=NO')

element = driver.find_element_by_name('tipo')
element.send_keys('Dados')

element = driver.find_element_by_name('tipoE')
element.send_keys('Concessionárias')

element = driver.find_element_by_name('distribuidora')
element.send_keys('370')

element = driver.find_element_by_name('periodo')
element.send_keys('Anual')
print(element)
# Printa os 20 primeiros caracteres na pagina
print('OK')
#driver.quit()
