from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
userwu_id = os.environ["USERWU_ID"]
userxiuwu_id = os.environ["USERXIUWU_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()

weather_remark="今天天气很好，出门可以愉快玩耍٩(˃̶͈̀௰˂̶͈́)و"
if wea.__contains__("多云"):
  weather_remark="今天天上很多棉花糖，适合去野外看风景(˶‾᷄ ⁻̫ ‾᷅˵)"
if wea.__contains__("阴"):
  weather_remark="今天天气阴，出门小心下雨( ･᷄ὢ･᷅ )"
if wea.__contains__("雨"):
  weather_remark="今天可能下雨，出门记得带伞哦(｡ ́︿ ̀｡)"
if wea.__contains__("大雨"):
  weather_remark="今天出門的話要注意看路上的水坑喔，不要貪玩！ಠ_ಠ"
if wea.__contains__("雷阵雨"):
  weather_remark="今天就不要出门啦，合法宅在家里♪(´ε｀ )！"
  
data = {"city":{"value":city},"weather_remark":{"value":weather_remark},"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
#resw = wm.send_template(userwu_id, template_id, data)
#resxw = wm.send_template(userxiuwu_id, template_id, data)
print(res)
#print(resw)
#print(resxw)
