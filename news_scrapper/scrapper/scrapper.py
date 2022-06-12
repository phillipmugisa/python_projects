"""
Author: Phillip Mugisa
Date: 6/08/2022

This program scraps news from top news platforms, the user is able to view news basing on location,
category

--requirements
    - beautifulsoup
    - requests

-- sources
    - google news
    - new york times
    - yahoo news

-- categories
    - technology
    - entertainment
    - fashion
    - sports
    - finance

-- locations
    - Global
    - USA
    - Europe
    - Africa

-- data structure
    {
        category: ______,
        count: ______,
        articles: [
            {
                'title' : ______,
                'description' : ______,
                'img_url' : ______,
            }
        ]
    }
    
"""
from cgitb import reset
from time import sleep
import requests
from bs4 import BeautifulSoup as bs
from typing import Dict
import concurrent.futures
import json


class ScrapperException(Exception):
    pass

class BaseScrapper(object):


    def __init__(self):
        self.categories = None
        self.article_attrs = None
        self.BASE_URL = None
        self.response = None

    @classmethod
    def get_name(cls):
        return cls.NAME
    
    @classmethod
    def set_name(cls, name):
        cls.NAME = name

    def get_base_url(self: object) -> str:
        if not self.BASE_URL:
            raise ScrapperException("No BASE URL FOUND")
        return self.BASE_URL

    def set_base_url(self: object, url: str) -> None:
        self.BASE_URL = url

    @classmethod
    def get_categories(self: object) -> Dict:
        if not self.categories:
            raise ScrapperException("No categories found")
        return self.categories
        
    @classmethod
    def set_categories(self: object, categories : Dict) -> None:
        self.categories = categories
    

    def fetch(self: object, url: str=None) -> None:
        if url:
            self.response = requests.get(url)
        else:
            self.response = requests.get(self.get_base_url)
        

    def get_response_status_code(self: object):
        if self.response:
            return self.response.status_code
        else:
            raise ScrapperException("No response data found")

    def get_response_content(self):
        if not self.response:
            raise ScrapperException("No response data found")
        return self.response.text

    def parse_content(self: object, data : str = None):
        if data:
            return bs(data, 'html.parser')

        if not self.response:
            raise ScrapperException("No response data found")
        else:
            return bs(self.get_response_content(), 'html.parser')

    def get_element(self: object, element : str, attrs = None, data : str = None) -> str:
        if data:
            # raises TypeError Exception if data is already parsed
            try:
                data = self.parse_content(data)
            except TypeError:
                pass
        else:
            data = self.parse_content()

        # find element
        if attrs and 'css' in attrs.keys():
            return data.select_one(attrs.get('css'))
        return data.find(element, attrs)

    def get_element_text(self: object, element : str) -> str:
        return element.getText()
        

    def get_elements(self: object, element : str, attrs = None, data : str = None) -> str:
        if data:
            # raises TypeError Exception if data is already parsed
            try:
                data = self.parse_content(data)
            except TypeError:
                pass
        else:
            data = self.parse_content()

        # find elements
        if attrs and 'css' in attrs.keys():
            return data.select(attrs.get('css'))
        return data.find_all(element, attrs)

    @classmethod
    def get_category_link(cls : object, category: str) -> str:
        if cls.categories.get(category):
            return cls.categories.get(category)
        raise ScrapperException("No category links found.")

    @classmethod
    def get_article_attrs(cls: object) -> str:
        if cls.article_attrs:
            return cls.article_attrs
        raise ScrapperException("No category attributes found.")

    @classmethod
    def set_article_attrs(cls: object, attrs: Dict) -> Dict:
        cls.article_attrs = attrs

    def get_elem_attrs(self, field):
        article_attrs = self.get_article_attrs()

        _elem = article_attrs.get(f'{field}').get('element')
        if article_attrs.get(f'{field}').get('css'):
            _attrs = {'css': article_attrs.get(f'{field}').get('css')}
        else:
            _attrs = {'class': article_attrs.get(f'{field}').get('class')}

        return _elem, _attrs

    def get_fetch_url(self, category):

        # get category link from instance variables
        category_link = self.get_category_link(category)

        return f'{self.get_base_url()}{category_link}'


    def scrap_category(self : object, category : str) -> Dict:
        
        # fetch data
        self.fetch(url = self.get_fetch_url(category))

        # get category attributes
        _element, _attrs = self.get_elem_attrs('article')
        
        articles = self.get_elements(element=_element, attrs=_attrs)

        # parse single article
        return self.build_result(articles, category)

    def get_article_link(self, element, category=None):
        return '{}{}'.format(self.get_base_url(), element.get('href', None))


    def build_result(self, articles, category):
        result = {'count': 0, 'category': category, 'articles': []}

        for article in articles:
            article_data = dict()
            try:
                for field in self.get_article_attrs().keys():
                    if field != 'article':
                        _element, _attrs = self.get_elem_attrs(field)
                        
                        article_elem = self.get_element(element=_element, attrs=_attrs, data = article)
                        if article_elem:
                            if field in ('title', 'description', 'date'):
                                if field == 'date':
                                    if hasattr(self, 'get_date'):
                                        article_data[f'{field}'] = self.get_date(element = article_elem)
                                else:
                                    article_data[f'{field}'] = article_elem.getText()
                                
                            elif field == 'url':
                                article_data[f'{field}'] = self.get_article_link(element = article_elem, category = category)
                            elif field == 'img_url':
                                article_data[f'{field}'] = article_elem.get('src', None)

                result['count'] += 1
                result['articles'].append(article_data)
            except Exception as Err:
                raise Err
        
        # with open(f'{self.__class__.__name__}-data.json', 'a', encoding='utf-8') as f:
        #     json.dump(result, f, ensure_ascii=False, indent=4)

        return result

    def run(self):
        # threads = []
        # for category in self.get_categories().keys():
        #     thread = Thread(target=self.scrap_category, args=[category])
        #     thread.start()
        #     threads.append(thread)
        #     sleep(5)

        # for thread in threads:
        #     thread.join()

        result = list()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = executor.map(self.scrap_category, self.get_categories().keys())

            for f in futures:
                result.append(f)
            pass

        return result

class NytScrapper(BaseScrapper):
    NAME = "New York Times"
    def __init__(self):
        # set base url
        self.set_base_url('https://www.nytimes.com')
        
        # set categories
        self.set_categories({
            'technology' : '/international/section/technology',
            'entertainment' : '/spotlight/pop-culture',
            'finance' : '/international/section/business',
            'sports' : '/international/section/sports',
            'fashion' : '/international/section/fashion',
            'health' : '/international/section/health'
        })

        # set article attributes
        self.set_article_attrs(
            {
                'article' : {'css' : 'li.css-112uytv', 'element' : 'li'},
                'url' : {'css': 'div.css-1l4spti a[href]', 'element' : 'a'},
                'date' : {'css': 'div.css-agsgss.e15t083i3 > span', 'element' : 'span'},
                'title' : {'css' : 'h2.css-1kv6qi.e15t083i0', 'element' : 'h2'},
                'description' : {'css' : 'p.css-1pga48a.e15t083i1', 'element' : 'p'},
                'img_url' : {'css': 'img.css-rq4mmj[src]', 'element' : 'img'},
            }
        )

class GoogleNewsScrapper(BaseScrapper):
    NAME = "Google News"
    def __init__(self):
        # set base url
        self.set_base_url('https://news.google.com/topics')

        # query parameters
        self.country = 'US'
        
        # set categories
        self.set_categories({
            'technology' : '/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGRqTVhZU0JXVnVMVWRDR2dKVlJ5Z0FQAQ',
            'entertainment' : '/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGRqTVhZU0JXVnVMVWRDR2dKVlJ5Z0FQAQ',
            'finance' : '/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGx6TVdZU0JXVnVMVWRDR2dKVlJ5Z0FQAQ',
            'sports' : '/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFp1ZEdvU0JXVnVMVWRDR2dKVlJ5Z0FQAQ',
            'health' : '/CAAqJQgKIh9DQkFTRVFvSUwyMHZNR3QwTlRFU0JXVnVMVWRDS0FBUAE'
        })

        # set article attributes
        self.set_article_attrs(
            {
                'article' : {'css' : 'div.NiLAwe.y6IFtc.R7GTQ.keNKEd.j7vNaf.nID9nc', 'element' : 'div'},
                'url' : {'css': 'a.DY5T1d.RZIKme', 'element' : 'a'},
                'date' : {'css': 'time.WW6dff.uQIVzc.Sksgp', 'element' : 'time'},
                'title' : {'css' : 'a.DY5T1d.RZIKme', 'element' : 'a'},
                'img_url' : {'css': 'figure.tvs3Id.QwxBBf', 'element' : 'figure'},
            }
        )

    def get_date(self, element):
        return element.datetime
        
    def get_article_link(self, element, category=None):
        return 'https://news.google.com{}'.format(element.get('href', None)[1:])

class YahooNewsScrapper(BaseScrapper):
    NAME = "Yahoo News"
    def __init__(self):
        # set base url
        # self.set_base_url('https://www.yahoo.com')

        # query parameters
        self.country = 'US'
        
        # set categories
        self.set_categories({
            'technology' : 'https://finance.yahoo.com/tech',
            'entertainment' : 'https://www.yahoo.com/entertainment',
            'finance' : 'https://finance.yahoo.com',
            'sports' : 'https://sports.yahoo.com'
        })

        # set article attributes
        self.set_article_attrs(
            {
                'article' : {'css' : 'li.js-stream-content div[data-test-locator="mega"]:not(.gemini-ad native-ad-item)', 'element' : 'div'},
                'url' : {'css': 'a.js-content-viewer', 'element' : 'a'},
                'description' : {'css' : 'p', 'element' : 'p'},
                'title' : {'css' : 'a.js-content-viewer', 'element' : 'a'},
                'img_url' : {'css': 'img[src]', 'element' : 'img'},
            }
        )

    def get_fetch_url(self, category):
        return self.get_category_link(category)

    def get_article_link(self, element, category=None):
        return '{}{}'.format(self.get_fetch_url(category), element.get('href', None))