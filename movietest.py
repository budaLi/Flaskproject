#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/7/5
import unittest
import time
from selenium import webdriver


class Hao123(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.base_url = "http://www.hao123.com/"
        self.verificationErrors = []

    # hao123 搜索用例
    def test_hao123_search(self):
        """hao123 搜索用例"""
        driver = self.driver
        # 进入hao123首页
        driver.get(self.base_url + "/")
        # 进行搜索
        driver.find_element_by_id("search-input").send_keys("selenium")
        driver.find_element_by_class_name("button-hook").click()
        time.sleep(2)
        driver.close()

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == '__main__':
    unittest.main()