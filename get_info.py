from parsel import Selector
import requests
from requests import Response
import re


# pip install parsel, requests


class parsing:
    def __init__(self, text):
        self.base_information = None
        self.final_list = None

        self.text = text
        self.url: str = "https://uk.wikipedia.org/wiki"
        self.new_url: str = self.url + "/" + self.text

        self.headers = self.get_headers()
        self.response: Response = self.make_request()
        self.data_list = self.parse()
        self.html: Response = requests.get(self.new_url)

    def make_request(self) -> Response:
        return requests.get(url=self.new_url, headers=self.headers)

    def get_headers(self) -> dict:
        return {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/122.0.0.0 Safari/537.36',
        }

    def parse(self) -> str:
        self.base_information = {}
        selector = Selector(text=self.response.text)

        base_information_main = selector.css('table.infobox tbody tr th::text').getall()
        base_information_info = selector.css('table.infobox tbody tr td::text').getall()

        for base_main, base_info in zip(base_information_main, base_information_info):
            self.base_information[base_main] = base_info

        print(self.base_information)

        information: str = str(selector.xpath('//*[@id="mw-content-text"]/div[1]/p[1]').get())
        information: Selector = Selector(text=information)
        clean_information = information.xpath('string()').extract_first()
        clean_information = re.sub(r'\[\d+\]', '', clean_information)

        self.final_list = clean_information + "\n" + self.new_url
        return self.final_list


def main() -> None:
    data_parse = parsing(text='Херсон')
    parsing_info = data_parse.data_list


if __name__ == '__main__':
    main()
