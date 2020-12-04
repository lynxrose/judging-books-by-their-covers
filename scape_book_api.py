import urllib, demjson, os, json, requests, time, random
import pandas as pd
import numpy as np
from urllib.request import urlopen

#date range of books
datelist = list(range(2009,2018))

#new york times best sellers
data = pd.read_json('nyt2.json', lines=True)

#information needed
author_title_best = data[['author','title']]

#drop duplicate best seller entries
author_title_best = author_title_best.drop_duplicates(subset=['title'])

#attempt to remove difficult charactors
author_title_best['author'].str.encode('ascii', 'ignore').str.decode('ascii')
author_title_best['title'].str.encode('ascii', 'ignore').str.decode('ascii')

#import random words to diversify book cover search
rand_word_text = open('randWords.txt', 'r').read()
rand_word_list = rand_word_text.split('\n')

# author_title_best
json_best = []
removelist = []
for i in range(len(author_title_best)):
    #search API using author and title
    author = author_title_best.iloc[i,0]
    title = author_title_best.iloc[i,1]
    url = f'''https://www.googleapis.com/books/v1/volumes?q=intitle:\"{title}\"+inauthor:{author}&maxResults=1'''
    url = url.replace(' ','%20')
    try:
        response = urllib.request.urlopen(url)
        temp_data = json.loads(response.read())
        json_best.append(temp_data)
        #pause around a second to not overload API
        time.sleep(random.uniform(.5, 1))
    except UnicodeEncodeError:
        #non ASCI charactors not removed from line 22-24
        continue

json_non = []
for word in rand_word_list:
    #take 100 books with relevents to random word (most books are not in data range)
    for i in range(100):
        url = f'''https://www.googleapis.com/books/v1/volumes?q={word}&maxResults=1&startIndex={i}'''
        response = urllib.request.urlopen(url)
        temp_data = json.loads(response.read())
        time.sleep(random.uniform(.5, 1))

#find the url, author, and title in the json file
def jsonParseBest(file):
    try:
        current = json.loads(json.dumps(file))['items']
        current = json.loads(json.dumps(current[0]))['volumeInfo']
        title = json.loads(json.dumps(current))['title']
        author = json.loads(json.dumps(current))['authors'][0]
        current = json.loads(json.dumps(current))['imageLinks']
        url = json.loads(json.dumps(current))['smallThumbnail']
        return url, title, author
    except KeyError:
        return 'fail', '', ''

def jsonParseNon(file):
    try:
        current = json.loads(json.dumps(file))['items']
        current = json.loads(json.dumps(current[0]))['volumeInfo']
        title = json.loads(json.dumps(current))['title']
        author = json.loads(json.dumps(current))['authors'][0]
        publishedDate = json.loads(json.dumps(current))['publishedDate']
        publishedYear = int(publishedDate[0:4])
        current = json.loads(json.dumps(current))['imageLinks']
        url = json.loads(json.dumps(current))['smallThumbnail']
        if ((title in best_sellers['title']) or (publishedYear not in datelist)):
            #removes best sellers and out of date range books
            return 'fail', '', ''
        else:
            return url, title, author
    except KeyError:
        return 'fail', '', ''
    except ValueError:
        return 'fail', '', ''

for idx, jsonFile in enumerate(json_best):
    curr_url, title, author = (jsonParseBest(jsonFile))
    if (curr_url == 'fail'):
        continue
    img_data = requests.get(curr_url).content
    #removes titles with '/' that confuse the jpg location
    title = title.replace('/',' ')
    with open(f'best_sellers_images/{title}.jpg', 'wb') as handler:
        handler.write(img_data)
    temp_df = pd.DataFrame([[title,author,f'{title}.jpg']],columns=['title','author','image'])
    best_sellers = non_best_sellers.append(temp_df)

# non_best_sellers = pd.DataFrame(columns=['title','author','image'])
for idx, jsonFile in enumerate(json_non):
    curr_url, title, author = (jsonParseBestNon(jsonFile))
    if (curr_url == 'fail'):
        continue
    img_data = requests.get(curr_url).content
    title = title.replace('/',' ')
    with open(f'non_best_sellers_images/{title}.jpg', 'wb') as handler:
        handler.write(img_data)
    temp_df = pd.DataFrame([[title,author,f'{title}.jpg']],columns=['title','author','image'])
    non_best_sellers = non_best_sellers.append(temp_df)


best_sellers['best'] = 0
non_best_sellers['best'] = 1
train = non_best_sellers.append(best_sellers)

train.to_csv('train.csv')