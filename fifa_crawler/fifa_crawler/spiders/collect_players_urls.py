import scrapy
from fifa_crawler.items import FifaCrawlerItem

class collect_player_url(scrapy.Spider):
  name='players_urls' 


  def start_requests(self):
    urls = 'https://sofifa.com/players?col=oa&sort=desc&offset=0'
    # YOUR CODE HERE
    #for url in urls:
    yield scrapy.Request(url=urls, callback = self.parse)
  def parse(self, response):
    # YOUR CODE HERE
    print("--------------")
    for href in response.xpath('//tbody/tr/td[@class="col-name"]/a[1]/@href').re(r'^/player/\d+'):
          #sel = scrapy.Selector(response)
          #item = FifaCrawlerItem()
          #item['player_url'] = href.split("/")[2]
          print(href)
          yield {
            'player_url': href}
         # yield response.follow(href, self.parse_player)
    offset = response.url[51:]
    print("offset",response.url[51:])
    urls = 'https://sofifa.com/players?col=oa&sort=desc&offset=0'
    if int(offset) < 660:
      next_url = urls[:-1] + str(int(offset)+60)
      yield scrapy.Request(url=next_url, callback = self.parse, dont_filter=True)
    # page = response.url.split('/')[-1]

