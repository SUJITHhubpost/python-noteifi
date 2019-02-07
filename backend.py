import requests
import csv
import time
from bs4 import BeautifulSoup
import re
import string
import pandas as pd 
from pandas.plotting import table
import matplotlib.pyplot as plt
import json 
import requests
import text_to_image



TOKEN = "620881300:AAGKrxtyBPjlEccDb1Vm2jtrULlsuLHru9Y"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates():
    url = URL + "getUpdates"
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def send_image(imageFile, chat_id):
    url = "https://api.telegram.org/bot620881300:AAGKrxtyBPjlEccDb1Vm2jtrULlsuLHru9Y/sendPhoto";
    files = {'photo': open(imageFile, 'rb')}
    data = {'chat_id' : chat_id}
    r= requests.post(url, files=files, data=data)

text, chat = get_last_chat_id_and_text(get_updates())
if(text == '/start'):
    send_message('Welcome to noteifi, This bot will give you updates on KU Notifications. This is one of the products by AiBlocks India private limited. The platform will be free to use. This is a beta version. Please send feedbacks to @sjx11', chat)



url1 = "https://exams.keralauniversity.ac.in/Login/check1"
headers = {'User-Agent': 'Mozilla/5.0'}

# Returns a requests.models.Response object
page = requests.get(url1, headers=headers)

soup = BeautifulSoup(page.text, 'lxml')  
lentd = len(soup.find_all('td', valign="top"))


while True:
    # Headers to mimic a browser visit

    
    titles = soup.find_all('tr', class_="tableHeading")
    notes = soup.find_all('tr', class_="displayList")
    
    list_titles = []
    for title in titles:
        title_td = title.find_all('td')
        str_title_td = str(title_td)
        clean = re.compile('<.*?>')
        clean2 = (re.sub(clean, '',str_title_td))
        list_titles.append(clean2)
        
        
        
    list_notes = []
    for note in notes:
            
        note_td = note.find_all('td', valign="top")
        str_note_td = str(note_td)
        clean3 = re.compile('<.*?>')
        clean4 = (re.sub(clean, '',str_note_td))
        list_notes.append(clean4)
    #pd.set_option('display.max_colwidth', 60)
    df = pd.DataFrame(list_notes)
    table = str.maketrans('', '' , string.punctuation)
    table = str.maketrans('','',"xa0\xa0\r\n\t\t\t\t\t'")
    stripped = [w.translate(table) for w in df[0]]
    p=df[df[0].str.contains("2013")==True]
    p=p[p[0].str.contains("B.Tech")==True]
    np = p.values
    dicter = p.to_string()
    encoded_image_path = text_to_image.encode(dicter, "image1.png")
        
    text, chat = get_last_chat_id_and_text(get_updates())
    send_image('/home/sj/Documents/products/noteifi/test.png', chat)
    send_message('Displaying Last {} notifications containing 2013 and B.Tech as tags'.format(len(np)), chat)
    
    for i in range(len(np)):
        send_message(np[i], chat)
       
        print(np[i])
    time.sleep(43200)

