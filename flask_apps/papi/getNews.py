from bs4 import BeautifulSoup as bs
import requests
from threading import Thread
from time import sleep
from papi.models import News, User
from papi import db


weblinks = { 
    'technology' : 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWUnlnQVAB',
    'sports' : 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FtVnVHZ0pWUnlnQVAB',
    'entertainment' : 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNREpxYW5RU0FtVnVHZ0pWUnlnQVAB'
}

def get_news(cat_title, url):
    print(f'Thread started for {cat_title}')

    news_count = 0
    # request for html page
    
    res = requests.get(url)

    # parse to html
    page = bs(res.text, 'html.parser')

    # pick articles
    news = page.select('.xrnccd')
    
    for idx, story in enumerate(news):
        if news_count < 10:
            try:
                story_title = story.find('h3', {'class' : 'ipQwMb ekueJc RD0gLb'}).select_one('.DY5T1d').getText()

                story_subtitle = story.select_one("h4.ipQwMb a").getText()

                discription = story.find("span", {"class" : "xBbh9"}).text

                story_img = story.find('img')['src']

                links = "https://news.google.com" + story.find('a', {'class': 'DY5T1d RZIKme'}).get('href', None)[1:]

                story_source = story.find('a', {'class': 'wEwyrc AVN2gc uQIVzc Sksgp'}).getText()

                c_news = News(
                    title=story_title,
                    subtitle=story_subtitle,
                    category=cat_title,
                    discription=str(discription),
                    source=story_source,
                    link=links,
                    story_img=story_img
                )
                print(c_news)
                db.session.add(c_news)
                db.session.commit()
                news_count += 1
            except:
                continue   

    print(f'Thread ended for {cat_title}, {news_count} news scrapped')

def run_scrapper():
    threads = []
    for cat_title, url in weblinks.items():
        t = Thread(target=get_news, args=[cat_title, url])
        t.start()
        threads.append(t)
        sleep(5)

    for thread in threads:
        thread.join()

