from urllib.parse import urlparse
from bs4 import BeautifulSoup as bS
from crawler.PxRequest import PxRequest
import pickle
import os


class URLSCrawler:

    baseURL = 'https://www.gsmarena.com/makers.php3'

    def __init__(self):
        self.urls_list = []
        url_parts = urlparse(URLSCrawler.baseURL)
        self.hostname = url_parts.hostname
        self.scheme = url_parts.scheme

        self.px_request = PxRequest()

        self.stage1_completed = False
        self.brand_links = dict()

        self.stage2_completed = False
        self.brand_pages = []

        self.stage3_completed = False
        self.item_pages = []

        if not os.path.isdir("saves"):
            os.mkdir("saves")

        if not os.path.isdir("saves//pages"):
            os.mkdir("saves//pages")

    def run_stage1(self):
        # get all main brand pages
        try:
            with open('saves\\brand_links.pickle', 'rb') as f:
                self.brand_links = pickle.load(f)
            self.stage1_completed = True
            print('  - saved stage 1 in use')
            return
        except FileNotFoundError:
            pass

        response = self.px_request.get(self.baseURL)
        soup = bS(response.text, 'lxml')
        brands_table = soup.find_all('div', class_='main main-makers l-box col float-right')
        self.brand_links = dict()

        for tag in brands_table:
            brand_list = tag.find_all('a')
            for brand in brand_list:
                self.brand_links[brand.text[:len(brand.text) - len(brand.span.text)]] = \
                    self.scheme + '://' + self.hostname+'/'+brand.get('href')
        self.stage1_completed = True

        with open('saves\\brand_links.pickle', 'wb') as f:
            pickle.dump(self.brand_links, f)
        print('  - stage 1 completed')

    def run_stage2(self):
        # get all brands pages
        if not self.stage1_completed:
            self.run_stage1()

        try:
            with open('saves\\brand_pages.pickle', 'rb') as f:
                self.brand_pages = pickle.load(f)
            self.stage2_completed = True
            print('  - saved stage 2 in use')
            return
        except FileNotFoundError:
            pass

        self.brand_pages = []

        for brand in self.brand_links:
            link = self.brand_links[brand]
            brand_page_response = self.px_request.get(link)
            brand_page_soup = bS(brand_page_response.text, 'lxml')
            brand_nav = brand_page_soup.find_all('div', class_='nav-pages')

            brand_page_links = [{'page': link, 'completed': False}]

            for page in brand_nav:
                pg_links = page.find_all('a')
                for pgLinkValue in pg_links:
                    brand_page_links.append(
                        {'page': self.scheme + '://' + self.hostname+'/'+pgLinkValue['href'], 'completed': False}
                    )

            self.brand_pages.append({'brand': brand, 'pages': brand_page_links})
            print(brand)

        self.stage2_completed = True

        with open('saves\\brand_pages.pickle', 'wb') as f:
            pickle.dump(self.brand_pages, f)
        print('  - stage 2 completed')

    def run_stage3(self):
        if not self.stage2_completed:
            self.run_stage2()

        try:
            with open('saves\\item_pages.pickle', 'rb') as f:
                self.item_pages = pickle.load(f)
            self.stage3_completed = True
            print('  - saved stage 3 in use')
        except FileNotFoundError:
            pass

        for brand in self.brand_pages:
            for page in [x for x in brand['pages'] if not x['completed']]:
                link = page['page']
                brand_page_response = self.px_request.get(link)
                brand_page_soup = bS(brand_page_response.text, 'lxml')
                brand_items = brand_page_soup.find_all('div', class_='makers')

                for point in brand_items:
                    item_links = point.find_all('li')

                    for item in item_links:
                        self.item_pages.append(
                            {
                                'brand': brand['brand'],
                                'item': self.scheme + '://' + self.hostname+'/'+item.a['href'],
                                'name': item.strong.span.text
                            }
                        )
                        page['completed'] = True

            with open('saves\\item_pages.pickle', 'wb') as f:
                pickle.dump(self.item_pages, f)
            with open('saves\\brand_pages.pickle', 'wb') as f:
                pickle.dump(self.brand_pages, f)

        self.stage3_completed = True
        print('  - stage 3 completed')

        
