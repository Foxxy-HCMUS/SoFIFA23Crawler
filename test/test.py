import json
import pandas as pd
# file = open('players_urls.json', 'r')
# log = json.load(file)
# file.close()
# file = open('players_urls_copy.json', 'r')
# correct_log = json.load(file)
# file.close()
# assert log == correct_log
# df_test = pd.read_json('players_info.json', encoding='utf-8-sig')
# print(df_test.iloc[0])

df_players_info = pd.read_json('fifa_crawler/dataset/players_info.json', encoding='utf-8-sig')
df_test = pd.read_json('test/players_info.json', encoding='utf-8-sig')
# assert df_players_info==df_test
s = "€20"
import re
print(re.match("^€",s))