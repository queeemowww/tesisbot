from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import asyncio

class Tracker():
    def __init__(self, awb_blank, awb_num, airport = None):
        self.awb_blank = awb_blank
        self.awb_num = awb_num
        self.airport = airport

    async def track_led(self):
        url = 'https://mirazh.pulkovo-cargo.ru/pls/apex/f?p=729:1::::::'

        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        browser = webdriver.Chrome(chrome_options)
        browser.get(url)

        awb_blank_elem = browser.find_element(By.ID, 'P1_BLANK')
        awb_num_elem = browser.find_element(By.ID, 'P1_NOMER')
        button_elem = browser.find_element(By.ID, 'B413105113012264023')

        awb_blank_elem.send_keys(self.awb_blank)
        awb_num_elem.send_keys(self.awb_num + Keys.RETURN)
        button_elem.click()

        route_elem = browser.find_element(By.ID, 'P1_APW_')
        report_els = browser.find_element(By.CSS_SELECTOR, '[class = "uReport uReportStandard"]')
        state_els = report_els.find_elements(By.TAG_NAME, 'tr')
        states = str('<b>' + route_elem.text + '</b>')
        for i in range(1, len(state_els)):
            states = states + '\n' + '<code>' +  str(i) + '. ' + state_els[i].text + '</code> '
        browser.quit()
        return states

# async def main():
#     tr = Tracker('216', '77131843')
#     l = await tr.track_led()
#     print(l)
# asyncio.run(main())