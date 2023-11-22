import os
import unittest
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

class TestStringMethods(unittest.TestCase):
        
    def test_is_returned(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto('https://www.reddit.com/r/vegas/comments/180a9mo/psa_avoid_using_cabs_like_the_plague_if_you_are/')
            
            page.screenshot(path="screenshot.png")

if __name__ == '__main__':
    unittest.main()