from parsel import Selector
import requests
from requests import Response
import re
import random
from key_user_agent import user_agent


# pip install parsel, requests


class parsing:
    def __init__(self, text, lang) -> None:
        text = re.sub(" ", "_", text)
        self.text = text
        self.lang = lang
        if self.lang == "ua":
            self.url: str = "https://uk.wikipedia.org/wiki"

        elif self.lang == "en":
            self.url: str = "https://en.wikipedia.org/wiki"

        self.new_url: str = self.url + "/" + self.text #https://en.wikipedia.org/wiki/Los_Angeles

        self.headers = self.get_headers()
        self.response: Response = self.make_request()

        self.html: Response = requests.get(self.new_url)
        self.selector = Selector(text=self.response.text)
        self.data_list = self.parse()
        self.photo = self.parse_photo()

    def make_request(self) -> Response:
        return requests.get(url=self.new_url, headers=self.headers)

    def get_headers(self) -> dict:
        return {
            'user-agent': str(random.sample(user_agent, 32))
        }

    def information(self) -> str:
        if self.lang == "ua":
            information: str = str(self.selector.xpath('//*[@id="mw-content-text"]/div[1]/p[1]').get())

        elif self.lang == "en":
            information: str = str(self.selector.xpath('//*[@id="mw-content-text"]/div[1]/p[2]').get())

        information: Selector = Selector(text=information)
        clean_information = information.xpath('string()').extract_first()
        clean_information = re.sub(r'\[\d+\]', '', clean_information)

        return clean_information + "\n" + self.new_url

    def parse_photo(self) -> str:
        photo: str = str(self.selector.css('.mw-body-content img').get(['src']))

        photo_link = re.findall(r'".+"', photo)

        for photo_link in photo_link:
            photo_link = photo_link

        if "src=" in photo_link:
            photo_link = re.findall(r'src=".+', photo_link)

            for photo_link in photo_link:
                photo_link = photo_link

            clear_photo_link = re.sub(r'"', '', photo_link)
            clear_photo_link = re.sub(r'src=', '', clear_photo_link)

        else:
            clear_photo_link = re.sub(r'"', '', photo_link)

        clear_photo_link = re.sub(r" .+", "", clear_photo_link)

        # clear_photo_link = re.sub(r".+ ")
        clear_photo_link = "https:" + clear_photo_link

        return clear_photo_link

    def parse(self) -> str:
        final_list = str(self.information())
        return final_list


# def main():
#     data = parsing(text="Лос Анджелес", lang="ua")
#
#     data_info: str = str(data.data_list)
#     data_photo: str = str(data.photo)
#
#     print(data_info)
#     print(data_photo)
#
#
# if __name__ == "__main__":
#     main()
