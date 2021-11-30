from crawler.GSMArena import URLSCrawler


if __name__ == '__main__':
    crawler = URLSCrawler()
    crawler.run_stage4()

    print(crawler.stage4_completed)
    print(crawler.px_request.proxy_using)
