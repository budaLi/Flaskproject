#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/7/5
#  要测试的函数：

import unittest

def sum(x, y):
    return x + y

def sub(x, y):
    return x - y

# 测试该函数的测试类
class mytest(unittest.TestCase):
    # setUp()初始化,
    def setUp(self):
        pass
    # 销毁
    def tearDown(self):
        pass
    # 具体的测试用例，以test开头
    def testsum(self):
        self.assertEqual(sum(1, 2), 44, 'test sum fail')

    def testsub(self):
        self.assertEqual(sub(2, 1), 1, 'test sub fail')

if __name__ == '__main__':
    unittest.main(2)