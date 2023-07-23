from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from db import iniciar_banco
import time, re
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def multithreaded_function(my_list,funcao):
    results = []

    with ThreadPoolExecutor() as executor:
        futures = []

        for item in my_list:
            future = executor.submit(funcao, item)
            futures.append(future)

        with tqdm(total=len(futures)) as pbar:
            for future in futures:
                result = future.result()
                results.append(result)
                pbar.update(1)
    return results

def salvar_no_banco(episodio:dict):
    try:
        db = iniciar_banco()
        cursor = db.cursor()
        cursor.execute(f"""INSERT INTO episodios_southpark (link_episodio,titulo,descricao,temporada,n_episodio,data_lancamento)
        values('{episodio['link_episodio']}','{episodio['titulo']}','{episodio['descricao']}','{episodio['temporada']}','{episodio['n_episodio']}','{episodio['data_lancamento']}')
        """)
        db.commit()
        db.close()
    except Exception as e:
        print(e)

def pegar_info_episodios(div_episodios):
    try:
        # print('------------------')
        ul = div_episodios.find_element(By.CSS_SELECTOR, 'ul')
        li = ul.find_elements(By.CSS_SELECTOR, 'li')
        episodios = []
        for item in li:            
            anchor = item.find_element(By.CSS_SELECTOR,'a')
            link_episodio = anchor.get_attribute('href')
            
            temp_ep = anchor.find_elements(By.CSS_SELECTOR,'h2')
            temp_ep = temp_ep[1].text
            temporada = re.findall(r"T\d*",temp_ep)[0]
            episodio = re.findall(r"E\d*",temp_ep)[0]

            nome_episodio = anchor.find_element(By.CSS_SELECTOR,'h3').text
            

            span_descricao = anchor.find_elements(By.CSS_SELECTOR,'span')
            descricao = ''
            data_lancamento = ''
            for span in span_descricao:
                texto = span.text
                if re.search(r"\d{2}\/\d{2}\/\d{4}",texto):
                    data_lancamento = texto
                if len(texto) >10:
                    descricao = texto

            # print(link_episodio)
            # print(temp_ep,nome_episodio)
            # print(descricao)
            # print(data_lancamento)

            episodios.append({
                'link_episodio': link_episodio,
                'titulo': nome_episodio.replace("'",""),
                'descricao': descricao.replace("'",""),
                'temporada': temporada.replace('T',''),
                'n_episodio': episodio.replace('E',''),
                'data_lancamento': data_lancamento
            })
            # div_descricao = partes[1]
            # header_descricao = div_descricao.find_element(By.TAG_NAME,'h2')
        return episodios
    except Exception as e:
        print(e)


def acessou_pegou(link_episodio:str):
    try:
        service = Service()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(service=service,options=chrome_options)
        driver.get(link_episodio)
        div_episodios = driver.find_element(By.CSS_SELECTOR,'div#content-episódios-completos-season')            
        info_episodios = pegar_info_episodios(div_episodios)
        for episodio in info_episodios:
            """"""
            salvar_no_banco(episodio)

    except Exception as e:
        print(e)

lista_links = []
try:
    service = Service()
    # driver = webdriver.Firefox(service=service)
    driver = webdriver.Chrome(service=service)

    driver.get('https://www.southparkstudios.com.br/seasons/south-park')

    dropdown = driver.find_element(By.CSS_SELECTOR,"div[data-testid='Dropdown']")
    drop_btn = dropdown.find_element(By.CSS_SELECTOR,"button")
    drop_btn.click()

    lista_itens = dropdown.find_element(By.CSS_SELECTOR,"ul")
    lista_itens = lista_itens.find_elements(By.CSS_SELECTOR,"li")
    temporadas = []

    print('Quantidade de temporadas:',len(lista_itens))



    for idx, temporada in enumerate(lista_itens):
        temporada = temporada.find_elements(By.CSS_SELECTOR,'a')
        if temporada:            
            temporada = temporada[0]
            link_temporada = temporada.get_attribute('href')
            # print(temporada.text)
            # print(link_temporada)
            if link_temporada:
                lista_links.append(link_temporada)

            if idx == 0:
                div_episodios = driver.find_element(By.CSS_SELECTOR,'div#content-episódios-completos-season')            
                episodios = pegar_info_episodios(div_episodios)            
                for episodio in episodios:
                    salvar_no_banco(episodio)
        
    # while True:
    #     True
    driver.close()
except Exception as e:
    print(e)
    driver.close()
    print('Fechou')

print('Temporadas:',len(lista_links))
multithreaded_function(my_list=lista_links,funcao=acessou_pegou)
print('Fim do codigo!')