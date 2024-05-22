from parsel import Selector
import requests
from requests import Response
import re
import random
from key_user_agent import user_agent


# pip install parsel, requests


class parsing:
    def __init__(self, text, lang):
        self.text = text
        self.lang = lang
        if self.lang == "ua":
            self.url: str = "https://uk.wikipedia.org/wiki"
            # print("Ukrainian")
        elif self.lang == "en":
            self.url: str = "https://en.wikipedia.org/wiki"
            # print("English")
        self.new_url: str = self.url + "/" + self.text

        self.headers = self.get_headers()
        self.response: Response = self.make_request()

        self.html: Response = requests.get(self.new_url)
        self.selector = Selector(text=self.response.text)
        self.data_list = self.parse()

    def make_request(self) -> Response:
        return requests.get(url=self.new_url, headers=self.headers)

    def get_headers(self) -> dict:
        return {
            'user-agent': str(random.sample(user_agent, 32))
        }

    # def right_menu(self):
    #     base_information = {}
    #
    #     base_information_main = self.selector.css('table.infobox tbody tr th::text').getall()
    #
    #     # print(base_information_main)
    #     # for clear_index in range(len(base_information_main)):
    #     #     print(clear_index)
    #     #     if '\n' in base_information_main[clear_index]:
    #     #         base_information_main[clear_index] = re.sub('\n', '', base_information_main[clear_index])
    #     #         if base_information_main[clear_index] == '':
    #     #             base_information_main.pop(clear_index)
    #     #             print(base_information_main)
    #
    #     # print(base_information_main)
    #
    #     base_information_info = self.selector.css('table.infobox tbody tr td::text').getall()
    #     # base_information_info = re.sub(r'\d+')
    #
    #     for base_main, base_info in zip(base_information_main, base_information_info):
    #         base_information[base_main] = base_info
    #
    #     return base_information

    def information(self):
        if self.lang == "ua":
            information: str = str(self.selector.xpath('//*[@id="mw-content-text"]/div[1]/p[1]').get())
        elif self.lang == "en":
            information: str = str(self.selector.xpath('//*[@id="mw-content-text"]/div[1]/p[2]').get())

        information: Selector = Selector(text=information)
        clean_information = information.xpath('string()').extract_first()
        clean_information = re.sub(r'\[\d+\]', '', clean_information)

        return clean_information + "\n" + self.new_url

    def parse(self) -> str:
        # print(self.selector.type)
        # final_list = "right_menu" + str(self.right_menu()) + "information" + str(self.information())
        final_list = str(self.information())
        return final_list
