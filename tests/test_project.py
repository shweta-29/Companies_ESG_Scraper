'''This module contains a class to test the scraper module'''
import unittest
import pandas as pd

from esgmetrics.esgscraper.scraper import WebScraper


class ScraperTestCase(unittest.TestCase):
    def setUp(self):
        self.scraper = WebScraper('https://carbontracker.org/')

    # @unittest.skip
    def test_init(self):
        expected_value = 'https://carbontracker.org/'
        actual_value = self.scraper.driver.current_url
        self.assertEqual(expected_value, actual_value)

    # @unittest.skip
    def test_wait_element_to_load(self):
        xpath = 'xyz'
        expected_value = None
        actual_value = self.scraper.wait_element_to_load(xpath)
        self.assertEqual(expected_value, actual_value)

    # @unittest.skip
    def test_convert_dict_to_csv(self):
        test_dict = {'A': [1], 'B': [2]}
        test_df = pd.DataFrame.from_dict(test_dict)
        expected_value = test_df
        actual_value = WebScraper.convert_dict_to_csv(test_dict, 'test')
        self.assertTrue(expected_value.equals(actual_value))

    # @unittest.skip
    def test_append_empty_values(self):
        test_dict = {'A': [1], 'B': [2]}
        expected_value = {'A': [1, None], 'B': [2, None]}
        actual_value = WebScraper.append_empty_values(test_dict)
        self.assertEqual(expected_value, actual_value)


if __name__ == '__main__':
    unittest.main()
