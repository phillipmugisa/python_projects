import unittest
from bs4 import BeautifulSoup as soup
from scrapper.scrapper import BaseScrapper, NytScrapper, GoogleNewsScrapper, YahooNewsScrapper

class TestScrapper(unittest.TestCase):

    def test_base_scrapper(self):
        base_scrapper = BaseScrapper()
        """
            bass scrapper class should contain the core functionalities like
                - make a request
                - extracting test from (an) element(s)
                - storing the scrapped data
        """
        # make request
        url = 'https://www.nytimes.com/international/section/technology'
        base_scrapper.fetch(url)
        self.assertEqual(200, base_scrapper.get_response_status_code())

        response_content = base_scrapper.get_response_content()
        self.assertIn("</html>", response_content.rstrip())

        # parse fetch passed data
        page = base_scrapper.parse_content("<html>a web page</html>")
        self.assertTrue(page)

        # parse fetch existing data
        _page = base_scrapper.parse_content()
        self.assertTrue(_page)

        # test_extract_data_from_element

        data = base_scrapper.parse_content('<b class="boldest">Extremely bold</b>')
        # the return data should contain a "b" element with test "Extremely"
        element = base_scrapper.get_element('b', {'class' : 'boldest'}, data=data)

        self.assertEqual('Extremely bold', base_scrapper.get_element_text(element))

        # locate multiple element
        data = '''<body><p class="title"><b>Body's title</b></p><p class="story">line begins<a class="element" href="http://example.com/element1"id="link1">1</a><a class="element" href="http://example.com/element2"id="link2">2</a><a class="element" href="http://example.com/element3"id="link3">3</a><p> line ends</p></p></body>'''

        self.assertEqual(3, len(base_scrapper.get_elements('a', data=data)))

    def test_nyt_scrapper(self):
        nyt_scrapper = NytScrapper()
        # nyt_scrapper must be an instance of BaseScrapper
        self.assertTrue(isinstance(nyt_scrapper, BaseScrapper))

        # set base url
        # self.assertFalse(nyt_scrapper.get_base_url())
        self.assertIn('nytimes', nyt_scrapper.get_base_url())

        self.assertIn('technology', nyt_scrapper.get_categories().keys())


        # self.assertTrue(isinstance(nyt_scrapper.scrap_category(category="fashion"), dict))

        # self.assertIn('count', nyt_scrapper.scrap_category(category="fashion").keys())
        # self.assertIn('category', nyt_scrapper.scrap_category(category="fashion").keys())
        # self.assertIn('articles', nyt_scrapper.scrap_category(category="fashion").keys())

        self.assertIn('description', nyt_scrapper.get_article_attrs().keys())

        nyt_scrapper.run()



    def test_google_news_scrapper(self):
        google_scrapper = GoogleNewsScrapper()
        # google_scrapper must be an instance of BaseScrapper
        self.assertTrue(isinstance(google_scrapper, BaseScrapper))

        # set base url
        # self.assertFalse(google_scrapper.get_base_url())
        self.assertIn('google', google_scrapper.get_base_url())

        self.assertIn('technology', google_scrapper.get_categories().keys())


        # self.assertTrue(isinstance(google_scrapper.scrap_category(category="fashion"), dict))

        # self.assertIn('count', google_scrapper.scrap_category(category="fashion").keys())
        # self.assertIn('category', google_scrapper.scrap_category(category="fashion").keys())
        # self.assertIn('articles', google_scrapper.scrap_category(category="fashion").keys())

        # self.assertIn('description', google_scrapper.get_article_attrs().keys())

        google_scrapper.run()


    def test_yahoo_news_news_scrapper(self):
        yahoo_news_scrapper = YahooNewsScrapper()
        # yahoo_news_scrapper must be an instance of BaseScrapper
        self.assertTrue(isinstance(yahoo_news_scrapper, BaseScrapper))

        # set base url
        # self.assertFalse(yahoo_news_scrapper.get_base_url())

        # self.assertIn('technology', yahoo_news_scrapper.get_categories().keys())


        # self.assertTrue(isinstance(yahoo_news_scrapper.scrap_category(category="fashion"), dict))

        # self.assertIn('count', yahoo_news_scrapper.scrap_category(category="fashion").keys())
        # self.assertIn('category', yahoo_news_scrapper.scrap_category(category="fashion").keys())
        # self.assertIn('articles', yahoo_news_scrapper.scrap_category(category="fashion").keys())

        self.assertIn('description', yahoo_news_scrapper.get_article_attrs().keys())

        yahoo_news_scrapper.run()



if __name__ == "__main__":
    unittest.main()