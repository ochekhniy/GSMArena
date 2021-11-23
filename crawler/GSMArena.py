from urllib.parse import urlparse
from bs4 import BeautifulSoup as bS
from crawler.PxRequest import PxRequest


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

    def run_stage1(self):
        # get all main brand pages
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

    def run_stage2(self):
        # get all brands pages
        if not self.stage1_completed:
            self.run_stage1()

        self.brand_pages = []

        for brand in self.brand_links:
            link = self.brand_links[brand]
            brand_page_response = self.px_request.get(link)
            brand_page_soup = bS(brand_page_response.text, 'lxml')
            brand_nav = brand_page_soup.find_all('div', class_='nav-pages')

            brand_page_links = [link, ]

            for page in brand_nav:
                pg_links = page.find_all('a')
                for pgLinkValue in pg_links:
                    brand_page_links.append(self.scheme + '://' + self.hostname+'/'+pgLinkValue['href'])

            self.brand_pages.append({'brand': brand, 'pages': brand_page_links})

            self.stage2_completed = True

    def run_stage3(self):
        if not self.stage2_completed:
            self.run_stage2()

        for brand, pages_list in self.brand_pages.items():
            for link in pages_list:
                print(link)
