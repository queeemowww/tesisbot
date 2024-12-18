from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import requests

class Tracker():
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_experimental_option("detach", True)
        self.browser = webdriver.Chrome(self.chrome_options)

    async def track_led(self, awb_blank, awb_num, airport = None):
        url = 'https://mirazh.pulkovo-cargo.ru/pls/apex/f?p=729:1::::::'
        if requests.get(url).status_code != 200:
            return 'В данный момент трекинг недоступен. Попробуйте позднее'

        # self.browser.execute_script(f'''window.open("{url}","_blank");''')
        self.browser.get(url)

        awb_blank_elem = self.browser.find_element(By.ID, 'P1_BLANK')
        awb_num_elem = self.browser.find_element(By.ID, 'P1_NOMER')
        button_elem = self.browser.find_element(By.ID, 'B413105113012264023')

        awb_blank_elem.send_keys(awb_blank)
        awb_num_elem.send_keys(awb_num + Keys.RETURN)
        button_elem.click()

        try:
            route_elem = self.browser.find_element(By.ID, 'P1_APW_')
            report_els = self.browser.find_element(By.CSS_SELECTOR, '[class = "uReport uReportStandard"]')
            state_els = report_els.find_elements(By.TAG_NAME, 'tr')
        except:
            self.browser.get(url)
            return 'Не удалось найти накладную с номером ' + '<code>' + awb_blank + '-' + awb_num + '</code>'
        # finally:
        #     self.browser.close()
        
        states = str('<b>' + route_elem.text + '</b>')
        for i in range(1, len(state_els)):
            states = states + '\n' + '<code>' +  str(i) + '. ' + state_els[i].text + '</code> '
        # self.browser.close()
        return states

# async def main():
#     tr = Tracker()
#     l = await tr.track_led('216', '77131843')
#     print(l)
# asyncio.run(main())