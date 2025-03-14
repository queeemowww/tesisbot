from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import requests
import asyncio
import time

class Tracker():
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_experimental_option("detach", True)
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.browser = webdriver.Chrome(self.chrome_options)

    async def track_led(self, awb_blank, awb_num):
        url = 'https://mirazh.pulkovo-cargo.ru/pls/apex/f?p=729:1::::::'
        if requests.get(url).status_code != 200 or (len(self.browser.find_elements(By.TAG_NAME, "center")) > 0 and self.browser.find_elements(By.TAG_NAME, "center")[0].text == "502 Bad Gateway"):
            return 'В данный момент трекинг недоступен. Попробуйте позднее'

        # self.browser.execute_script(f'''window.open("{url}","_blank");''')
        self.browser.get(url)

        awb_blank_elem = self.browser.find_element(By.ID, 'P1_BLANK')
        awb_num_elem = self.browser.find_element(By.ID, 'P1_NOMER')
        button_elem = self.browser.find_element(By.ID, 'B413105113012264023')

        awb_blank_elem.send_keys(awb_blank)
        awb_num_elem.send_keys(awb_num + Keys.RETURN)
        button_elem.click()
        time.sleep(.5)

        try:
            route_elem = self.browser.find_element(By.CSS_SELECTOR, '[class = "display_only apex-item-display-only"]')
            report_els = self.browser.find_element(By.CSS_SELECTOR, '[class = "uReport uReportStandard"]')
            state_els = report_els.find_elements(By.TAG_NAME, 'tr')
            states = str('<b>' + route_elem.text + '</b>')
            for i in range(1, len(state_els)):
                states = states + '\n' + '<code>' +  str(i) + '. ' + state_els[i].text + '</code>'
            return states
        except Exception as e:
            print(e)
            return 'Не удалось найти накладную с номером ' + '<code>' + awb_blank + '-' + awb_num + '</code>'
        finally:
            self.browser.close()

    async def track_svo(self, awb_blank = None, awb_num = None):
        url = 'https://www.moscow-cargo.com/'
        
        if requests.get(url).status_code != 200:
            return 'В данный момент трекинг недоступен. Попробуйте позднее'
        self.browser.get(url)

        awb_blank_elem = self.browser.find_element(By.CSS_SELECTOR, '[class = "awb-prefix awb-part"]')
        awb_num_elem = self.browser.find_element(By.CSS_SELECTOR, '[class = "awb-number awb-part"]')

        awb_blank_elem.send_keys(awb_blank)
        awb_num_elem.send_keys(awb_num + Keys.RETURN)

        time.sleep(2)
        try:
            state_els = self.browser.find_elements(By.CSS_SELECTOR, '[id = "status"]')
            status = state_els[0].find_elements(By.TAG_NAME, "tr")
            states = ''
            for i in range(len(state_els[0].find_elements(By.TAG_NAME, "tr"))):
                states = states + '\n' + '<code>' +  str(i + 1) + '. ' + status[i].text + '</code>'
            return states
        except Exception as e:
            print(e)
            return 'Не удалось найти накладную с номером ' + '<code>' + awb_blank + '-' + awb_num + '</code>'
        finally:
            self.browser.close()

# async def main():
#     tr = Tracker()
#     # l = await tr.track_led('216', '77131843')
#     m = await tr.track_svo('555', '08392230')
#     # print(l)
#     print(m)
    
# asyncio.run(main())