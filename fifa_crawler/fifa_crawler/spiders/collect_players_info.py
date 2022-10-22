import scrapy
import json
import re

class collect_player_info(scrapy.Spider):
  name='players_info'
  
  def __init__(self):
    try:
      with open('dataset/players_urls.json') as f:
        self.players = json.load(f)
      self.player_count = 1
    except IOError:
      print("File not found")

  def start_requests(self):
    urls = ['https://sofifa.com/player/231747?units=mks']
    # YOUR CODE HERE
    urls[0] = urls[0].replace('/player/231747',self.players[0]['player_url'])
    for url in urls:
        yield scrapy.Request(url,callback=self.parse,dont_filter=True)
  def parse(self, response):
      # YOUR CODE HERE
      # Nguồn tham khảo: https://github.com/sauravhiremath/fifa-stats-crawler/blob/master/fifa-crawler/fifa_parser/spiders/players_stats.py
      print(response.css)
      info = response.xpath('//div[@class="info"]//text()').getall()[-2]
      # split_info = info.split()
      # split_age = split_info[0][:-4]
      # split_bd = split_info[3].replace(')','/') + split_info[1].replace('(','')+'/' + split_info[2].replace(',','')
      # split_height = re.match('(\d+)cm',split_info[4])
      # split_weight = re.match('(\d+)kg',split_info[5])
      split_info = re.findall(' (\d+)y.o. [(](\w+) (\d+), (\d+)[)] (\d+)cm (\d+)kg', info)
      split_info = list(split_info[0])
      split_age = split_info[0]
      split_bd = split_info[3] + '/' + split_info[1] + '/' + split_info[2]
      split_height = split_info[4]
      split_weight = split_info[5]
      # lấy đội bóng của cầu thủ
      teams_name = response.xpath('//div[@class="card"]//h5//a/text()').getall()
      teams_value = response.xpath('//div[@class="card"]//ul[@class="ellipsis pl"]//li[1]/span[1]/text()').getall()
      teams_value = list(map(int,teams_value))  # chuyển list string thành list integer
      teams = dict(zip(teams_name,teams_value)) # tạo 1 dict với key là tên đội và value là đánh giá đội
      number_traits = len(response.xpath('//div[@class="card" and h5="Traits"]//li').getall())
      number_specialities = len(response.xpath('//div[@class="card" and h5="Player Specialities"]//li').getall())
      
      props = {}
      props_key = response.xpath('//div[@class="card" and h5!="Profile" and h5!="Traits" and not(img)]//ul/li/span[last()]/text()').getall()
      props_key = [x.replace(' ','') for x in props_key]
      props_value = response.xpath('//div[@class="card" and h5!="Profile" and h5!="Traits" and not(img)]//ul//li/span[1]/text()').getall()
      props_value = list(map(int,props_value)) 
      props = dict(zip(props_key,props_value))
      # number_goalkeeping = len(response.xpath('//div[@class="card" and h5="Goalkeeping"]//li').getall())
      # goalkeeping = {}
      # for i in range(1, number_goalkeeping+1):
      #     goalkeeping[response.xpath('//div[@class="card" and h5="Goalkeeping"]//li['+str(i)+']/span[last()]/text()').get().replace(' ','')] =int(response.xpath('//div[@class="card" and h5="Goalkeeping"]//li['+str(i)+']/span[1]/text()').get())
      yield {             
        "id": response.xpath('//div[@class="card" and h5="Profile"]//li[label = "ID"]/text()').get(),
        "name": response.css("div.info h1::text").get(default=''),
        "primary_position": response.xpath('//div[@class="col col-4"]//li[label="Best Position"]/span/text()').get(),
        "positions": response.xpath('//div[@class="info"]//span/text()').getall(),#response.xpath('//div[@class="card" and ul[@class="ellipsis pl"]]//li[label="Position"]/span/text()').getall(),
        "age": split_age,
        "birth_date": split_bd,
        "height": int(split_height),
        "weight": int(split_weight),
        "Overall Rating": int(response.xpath('//section[@class="card spacing"]//div[1]//span/text()').get()),
        "Potential": int(response.xpath('//section[@class="card spacing"]//div[2]//span/text()').get()),
        "Value": response.xpath('//section[@class="card spacing"]//div[3]/div/text()').get(),
        "Wage": response.xpath('//section[@class="card spacing"]//div[4]/div/text()').get(),
        "Preferred Foot": response.xpath('//div[@class="card" and h5="Profile"]//li[label = "Preferred Foot"]/text()').get(),
        "Weak Foot": int(response.xpath('//div[@class="card" and h5="Profile"]//li[label = "Weak Foot"]/text()').get()),
        "Skill Moves": int(response.xpath('//div[@class="card" and h5="Profile"]//li[label = "Skill Moves"]/text()').get()),
        "International Reputation": int(response.xpath('//div[@class="card" and h5="Profile"]//li[label = "International Reputation"]/text()').get()),
        "Work Rate": response.xpath('//div[@class="card" and h5="Profile"]//li[label = "Work Rate"]/span/text()').get(),
        "Body Type": response.xpath('//div[@class="card" and h5="Profile"]//li[label = "Body Type"]/span/text()').get(),
        "Real Face": response.xpath('//div[@class="card" and h5="Profile"]//li[label = "Real Face"]/span/text()').get(),
        "Release Clause": response.xpath('//div[@class="card" and h5="Profile"]//li[label = "Release Clause"]/span/text()').get(),
        "teams": teams,
        "attacking": dict(list(props.items())[:5]),
        "skill": dict(list(props.items())[5:10]),
        "movement": dict(list(props.items())[10:15]),
        "power": dict(list(props.items())[15:20]),
        "mentality": dict(list(props.items())[20:26]),
        "defending": dict(list(props.items())[26:29]),
        "goalkeeping": dict(list(props.items())[29:34]), 
        "player_traits": [response.xpath('//div[@class="card" and h5="Traits"]//li['+str(i)+']//span/text()').get() for i in range(1,number_traits+1)],
        "player_specialities": [response.xpath('//div[@class="card" and h5="Player Specialities"]//li['+str(i)+']//a/text()').get() for i in range(1,number_specialities+1)],
      }
          
      if self.player_count < len(self.players):
        next_page_url = 'https://sofifa.com' + self.players[self.player_count]['player_url'] + '?units=mks'
        self.player_count += 1
        yield scrapy.Request(url=next_page_url, callback=self.parse) 