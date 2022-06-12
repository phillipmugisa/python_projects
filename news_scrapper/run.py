from scrapper.scrapper import BaseScrapper, NytScrapper, GoogleNewsScrapper, YahooNewsScrapper
import json

def main():
    nyt_scrapper = NytScrapper()
    google_scrapper = GoogleNewsScrapper()
    yahoo_news_scrapper = YahooNewsScrapper()

    for cls in [nyt_scrapper, google_scrapper, yahoo_news_scrapper]:
        filename = '{}'.format('-'.join(cls.get_name().split(' ')))
        with open(f'{filename}.json', 'a', encoding='utf-8') as f:
            json.dump(cls.run(), f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()