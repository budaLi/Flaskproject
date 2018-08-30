#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/7/5
import unittest, doctest
import HTMLTestRunner
import movietest
import test_baidu
# 构造测试套件
suite = doctest.DocTestSuite()

# 罗列要执行的文件
suite.addTest(unittest.makeSuite(test_baidu,))
# suite.addTest(unittest.makeSuite(test_hao123.Hao123))

filename = "D://result.html"
with open(filename, "wb") as fp:
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        title="Report_title",
        description="Report_description"
    )
    runner.run(suite)