import os
import unittest
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

class TestScreenshot(unittest.TestCase):
        
    def test_is_returned(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto('https://www.reddit.com/r/confessions/comments/181gg06/my_mom_unknowingly_destroyed_my_porn_stash/')
            page.wait_for_load_state()
            page.wait_for_selector('shreddit-post')
            page.locator('shreddit-post').screenshot(path="scr3eenshot.png")

if __name__ == '__main__':
    unittest.main()