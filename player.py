from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

class Player():
    def __init__(self,link_episodio,volume,navegador) -> None:
        self._link_episodio = link_episodio
        self._volume = volume
        self._navegador = navegador
        self._driver = self._iniciar_navegador()
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

    def _checar_se_acabou(self)->bool:
        try:
            total_videos = self._driver.find_elements(By.CSS_SELECTOR, 'video')
            video_element = total_videos[0]
            has_ended = self._driver.execute_script("return arguments[0].duration;", video_element)
            # print(has_ended)
            if not has_ended:
                return True
            else:
                return None
        except Exception as e:
            print(e)
            return None

    def executar_video(self):
        try:            
            time.sleep(10)
            total_videos = self._driver.find_elements(By.CSS_SELECTOR, 'video')
            video_element = total_videos[0]
            # video_element = WebDriverWait(self._driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "video")))            
            # print('Achei videos?',video_element)
            pausado = self._driver.execute_script("return arguments[0].paused;", video_element)
            action_chains = ActionChains(self._driver)
            action_chains.move_to_element(video_element).click().perform()

            self._driver.execute_script("return arguments[0].requestFullscreen();", video_element)
            self._driver.execute_script("arguments[0].muted = false;", video_element)
            video_element.click()

            self._driver.execute_script("arguments[0].play();", video_element)

            
            self._driver.execute_script("arguments[0].volume = 0.3;", video_element)
            
            ended = self._checar_se_acabou()
            while not ended:
                ended = self._checar_se_acabou()

            self._driver.close()
        except Exception as e:
            print(e)