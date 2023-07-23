from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

class Player():
    def __init__(self,link_episodio,volume,navegador) -> None:
        self._link_episodio = link_episodio
        self._volume = volume
        self._navegador = navegador
        self._driver = None
        pass

    def _iniciar_navegador(self)-> webdriver:
        try:
            service = Service()
            if self._navegador == 'firefox':
                driver = webdriver.Firefox(service=service)
            elif self._navegador == 'chrome':
                driver = webdriver.Chrome(service=service)
            elif self._navegador == 'edge':
                driver = webdriver.Edge(service=service)
            else:
                return None

            driver.get(self._link_episodio)
            self._driver = driver
            return driver
        except Exception as e:
            print(e)

    def executar_video(self):
        try:
            video_element = WebDriverWait(self._driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "video")))            
            print('Achei videos?',video_element)
            div_element = self._driver.find_elements(By.CSS_SELECTOR, 'div[aria-label="Video player"]')
            print('Divs de video',len(div_element))
            self._driver.execute_script("arguments[0].muted = true;", video_element)

            div_element = div_element[0]
            div_element.click()
            time.sleep(3)            
            self._driver.execute_script("arguments[0].requestFullscreen();", video_element)
            self._driver.execute_script("arguments[0].muted = false;", video_element)
            self._driver.execute_script("arguments[0].volume = 0.3;", video_element)
            time.sleep(10)                        
            duration = self._driver.execute_script("return arguments[0].duration;", video_element)
            print(duration)
            has_ended = self._driver.execute_script("return arguments[0].ended;", video_element)
            print('Acabou?',has_ended)
            while not has_ended:
                has_ended = self._driver.execute_script("return arguments[0].ended;", video_element)

            print('Acabou!!!')
                            
            # self._driver.execute_script("arguments[0].play();", video_element)
        except Exception as e:
            print(e)