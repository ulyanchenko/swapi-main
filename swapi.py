import requests
from pathlib import Path


class APIRequester:

    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, url):
        try:
            response = requests.get(self.base_url + url)
            response.raise_for_status()
            return response
        except requests.ConnectionError:
            print('<сетевая ошибка>')
        except requests.HTTPError:
            print('<ошибка на сервере>')
        except requests.RequestException:
            print('Возникла ошибка при выполнении запроса')


class SWRequester(APIRequester):

    def get_sw_categories(self):
        response = self.get('/')
        return response.json().keys()

    def get_sw_info(self, sw_type):
        response = self.get('/' + sw_type + '/')
        return response.text


def save_sw_data():
    sw_url = SWRequester('https://swapi.dev/api')
    Path('data').mkdir(exist_ok=True)
    for category in sw_url.get_sw_categories():
        with open(f'data/{category}.txt', 'w', encoding='utf8') as file:
            sw_type = category
            file.write(sw_url.get_sw_info(sw_type))
