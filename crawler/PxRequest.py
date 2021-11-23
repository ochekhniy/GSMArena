from fake_useragent import UserAgent
from requests import get as get_request
from bs4 import BeautifulSoup as bS
from random import choice as random_choice


def un_static_method(static):
    return static.__get__(None, object)


class PxRequest:
    _instance = None

    @staticmethod
    def get_proxy_list_from_fox_tools():
        proxy_cite_url = 'http://foxtools.ru/Proxy?al=False&am=False&ah=True&ahs=True&http=True&https=True&page='
        page = 1
        local_proxy_list = []
        while True:
            response = get_request(proxy_cite_url+str(page))
            soup = bS(response.text, 'lxml')

            if soup.find('div', class_='nodata'):
                break

            table = soup.find('table', id='theProxyList')
            if table is None:
                break

            t_body = table.tbody
            if t_body is None:
                break

            rows = t_body.find_all('input', class_='ch')

            for row in rows:
                proxy_dict = {
                    "http": 'http://'+row['value']
                }

                local_proxy_list.append(proxy_dict)
            page += 1
        return local_proxy_list

    default_get_proxy_func = un_static_method(get_proxy_list_from_fox_tools)

    def __init__(self, get_proxy_func=default_get_proxy_func):
        self.proxy_list = get_proxy_func()
        self.timeout = 5
        self.proxy_using = dict()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def get(self, the_url):
        while True:
            if len(self.proxy_list):
                chosen_proxy = random_choice(self.proxy_list)
                response = get_request(
                    the_url,
                    headers={'User-Agent': UserAgent().random},
                    timeout=self.timeout,
                    proxies=chosen_proxy,
                    allow_redirects=True,
                )
                if response.status_code < 400:
                    self.proxy_using[chosen_proxy['http']] = self.proxy_using.get(chosen_proxy['http'], 0) + 1
                    return response
                else:
                    self.proxy_list.remove(chosen_proxy)
            else:
                raise Exception('Empty proxy list')


if __name__ == '__main__':
    pxRequest1 = PxRequest()
    result = pxRequest1.get('https://www.gsmarena.com/makers.php3')
    print(result.status_code)
    print(pxRequest1.proxy_using)
