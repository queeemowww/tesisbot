import os
import asyncio
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
# from database.db_provider import get_db
import time
import re


class Tracker():
    def __init__(self, delay = None):
        self.base_url = "https://mirazh.pulkovo-cargo.ru/pls/apex/f?p=729:1::::::"
        self.browser = None
        self.page = None

    async def launch_browser(self):
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=False)
        self.page = await self.browser.new_page()

    async def close_browser(self):
        if self.browser:
            await self.browser.close()

    async def track_svo(self, awb):
        await self.launch_browser()
        await self.page.goto(self.base_url)
        awb_blank_elem = await self.page.query_selector_all('[class = "awb-prefix awb-part"]')
        awb_num_elem = await self.page.query_selector_all('[class = "awb-number awb-part"]')
        await awb_blank_elem[0].fill(awb[:3])
        await awb_num_elem[0].fill(awb[3:])
        await self.page.locator('button[id = "getstatus"]').click()
        await self.page.wait_for_selector('div[class = "modal fade bd-status_sub-lg show"]')
        tbody = await self.page.query_selector('tbody[id = "statusbody"]')
        tds = await tbody.query_selector_all('td')
        if len(tds) <= 2:
            return 'ND'
        return str(await tds[-1].inner_text()).replace("\n", "/")
    
    async def track_led(self, awb):
        await self.launch_browser()
        await self.page.goto(self.base_url)
        awb_blank_elem = await self.page.query_selector_all('[id = "P1_BLANK"]')
        awb_num_elem = await self.page.query_selector_all('[id = "P1_NOMER"]')
        await awb_blank_elem[0].fill(awb[:3])
        await awb_num_elem[0].fill(awb[4:])
        await self.page.locator('[id = "B413105113012264023"]').click()
        route_elem = await self.page.query_selector("[class = 'display_only apex-item-display-only']")
        report_els = await self.page.query_selector('[class = "uReport uReportStandard"]')
        state_els = await report_els.query_selector_all('tr')
        states = str('<b>' + await route_elem.inner_text() + '</b>')
        for i in range(1, len(state_els)):
            states = states + '\n' + '<code>' +  str(i) + '. ' + await state_els[i].inner_text() + '</code>'
        await self.close_browser()
        return states


if __name__ == '__main__':
    tr = Tracker()
    print(asyncio.run(tr.track_led('421-78336425')))


# async def main():
#     tr = Tracker()
#     # l = await tr.track_led('216', '77131843')
#     m = await tr.track_svo('555', '08392230')
#     # print(l)
#     print(m)
    
# asyncio.run(main())