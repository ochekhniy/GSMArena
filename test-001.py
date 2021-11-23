import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from fake_useragent import UserAgent

baseURL = 'https://www.gsmarena.com/makers.php3'

urlParts = urlparse(baseURL)
hostname = urlParts.hostname
scheme = urlParts.scheme

response = requests.get(baseURL, headers={'User-Agent': UserAgent().chrome})
soup = BeautifulSoup(response.text, 'lxml')

brandsTable = soup.find_all('div', class_='main main-makers l-box col float-right')

brandLinks = {}

# decomposition to brands
for tag in brandsTable:
    brandList = tag.find_all('a')
    for brand in brandList:
        brandLinks[brand.text[:len(brand.text) - len(brand.span.text)]] = scheme + '://' + hostname+'/'+brand.get('href')

# decomposition to pages

pagesToParse = []
for brand in brandLinks:
    link = brandLinks[brand]
    brandPageResponse = requests.get(link, headers={'User-Agent': UserAgent().chrome})
    brandPageSoup = BeautifulSoup(brandPageResponse.text, 'lxml')
    brandNav = brandPageSoup.find_all('div', class_='nav-pages')

    brandPageLinks = [link, ]

    for page in brandNav:
        pgLinks = page.find_all('a')
        for pgLinkValue in pgLinks:
            brandPageLinks.append(scheme + '://' + hostname+'/'+pgLinkValue['href'])

    pagesToParse.append({'brand': brand, 'pages': brandPageLinks})

print(len(pagesToParse))
