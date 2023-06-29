from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

service = Service()
driver = webdriver.Firefox(service=service)

driver.get('https://www.southparkstudios.com.br/seasons/south-park')

dropdown = driver.find_element(By.CSS_SELECTOR,"div[data-testid='Dropdown']")
dropdown.click()
lista_itens = dropdown.find_element(By.CSS_SELECTOR,"ul")
lista_itens = lista_itens.find_elements(By.CSS_SELECTOR,"li")

# for temporada in lista_itens:


print("Total de temporadas:",len(lista_itens))
while True:
    True