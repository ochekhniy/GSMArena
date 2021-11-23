from crawler.GSMArena import URLSCrawler


if __name__ == '__main__':
    crawler = URLSCrawler()
    crawler.run_stage2()

    print(crawler.brand_links)
    print(crawler.brand_pages)
    print(crawler.px_request.proxy_using)
