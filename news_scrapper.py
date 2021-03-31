from bs4 import BeautifulSoup as bs
import requests
import json
from twilio.rest import Client
import time

weblinks = { 
    'technology' : 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWUnlnQVAB',
    'sports' : 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FtVnVHZ0pWUnlnQVAB',
    'entertainment' : 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNREpxYW5RU0FtVnVHZ0pWUnlnQVAB'
}

def get_news(url):
    # request for html page
    res = requests.get(url)

    # parse to html
    page = bs(res.text, 'html.parser')

    # pick articles
    news = page.select('.xrnccd')

    data = {}
    for idx, story in enumerate(news):
        if idx < 20:
            story_title = story.find('h3', {'class' : 'ipQwMb ekueJc RD0gLb'}).select_one('.DY5T1d').getText()


            story_subtitle = story.select_one("h4.ipQwMb a").getText() if story.select_one("h4.ipQwMb a") else 'Not Found'

            discription = story.find("span", {"class" : "xBbh9"}).text if story.find("span", {"class" : "xBbh9"}) else "Not Found"

            story_img = story.find('img')['src'] if story.find('img') else "Not Found"

            links = "https://news.google.com" + story.find('a', {'class': 'DY5T1d RZIKme'}).get('href', None)[1:]

            story_source = story.find('a', {'class': 'wEwyrc AVN2gc uQIVzc Sksgp'}).getText()

            # store data
            data[idx] = {
                'title' : story_title,
                'subtitle' : story_subtitle,
                'source' : story_source,
                'discription' : str(discription),
                'link' : links,
                'story_img' : story_img
            }
        else:
            break

    # with open('data.json', 'w') as file:
    #     json.dump(data, file, indent=4, sort_keys=True)

    return data

def send_news(news):
    try:    
        account_sid = 'ACe7c7bffe4cfd9e0672f2426a95a8d4bf' 
        auth_token = '3ac63f355758eb88c8858bf7963b4a36' 
        client = Client(account_sid, auth_token) 
        
        message = client.messages.create( 
                                    from_='whatsapp:+14155238886',    
                                    media_url = [news['story_img']] if news['story_img'] != 'Not Found' else "",
                                    body=f"*{news['title']}* \n *{news['subtitle']}* \n_{news['discription']}_ \n{news['link']} \n{news['source']}",      
                                    to='whatsapp:+256757375684',
                                ) 
        
        print(message.sid)
    except Exception as err:
        account_sid = 'ACe7c7bffe4cfd9e0672f2426a95a8d4bf' 
        auth_token = '3ac63f355758eb88c8858bf7963b4a36' 
        client = Client(account_sid, auth_token) 
        
        message = client.messages.create( 
                                    from_='whatsapp:+14155238886',    
                                    body=f"*{err}*",      
                                    to='whatsapp:+256757375684',
                                ) 
        main()

def main():
    for _, url in weblinks.items():
        news = get_news(url)
        for item in news.values():
            send_news(item)

if __name__ == "__main__":
    while True:
        try:
            main()
            time.sleep(3600)
        except Exception as err:
            account_sid = 'ACe7c7bffe4cfd9e0672f2426a95a8d4bf' 
            auth_token = '3ac63f355758eb88c8858bf7963b4a36' 
            client = Client(account_sid, auth_token) 
            
            message = client.messages.create( 
                                        from_='whatsapp:+14155238886',    
                                        body=f"*{err}*",      
                                        to='whatsapp:+256757375684',
                                    ) 
            continue