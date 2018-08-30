#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium import webdriver  #再Python selenium官网中可以看到
from selenium.webdriver.common.by import By
from pyquery import PyQuery as pq
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC#下载chromdriver 并放到项目下
import datetime
browser=webdriver.Chrome()   #加载谷歌浏览器
wait=WebDriverWait(browser,10)  #等待十秒时间加载页面
import time
import json
import re

register_list={             #注册测试

        'name':3332,
        'email':'1364823355@qq.com',
        'phone':14744656225,
        'pwd':1,
        'pwd_again':1,

    }
change_info={
        'name':2,
        'email':'1356666666@qq.com',
        'phone':1575555555,
        'info':'123'
    }
change_pwd={
        'name':23,
        'old_pwd':1,
        'new_pwd':333,
        'new_pwd_again':333,
    }
admin_login_ingo={
        'name':u'李不搭',
        'pwd':'zslswmz'
    }
tag_name={
        'name':u'韩国'
    }
movie_add_info={
        'title':u'一个人的武林',
        'url':'C:\\Users\\Lenovo\\Desktop\\movie\\1.mp4',
        'logo':'C:\\Users\\Lenovo\\Desktop\\big0720150102210934.jpg',
        'info':u'王宝强主演',
        'lenth':145,
        'area':u'中国',
        'addtime':'2017-03-05'
    }
movie_edit_info={
        'title':u'江湖',
        'url':'C:\\Users\\Lenovo\\Desktop\\movie\\2.mp4',
        'logo':'C:\\Users\\Lenovo\\Desktop\\big0720150102210934.jpg',
        'info':u'江湖传说',
        'lenth':145,
        'area':u'中国',
        'addtime':'2017-03-05'
    }
class Baidu(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(self)
        self.driver.implicitly_wait(30)
        self.base_url = "http://www.baidu.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

        # # 百度搜索用例
        # def test_baidu_search(self):
        #     """百度搜索用例"""
        #     driver = self.driver
        #     # 进入百度首页
        #     driver.get(self.base_url + "/")
        #     # 进行搜索
        #     try:
        #         driver.find_element_by_id("kw").send_keys("selenium webdriver")
        #         driver.find_element_by_id("su").click(self)
        #     except:
        #         driver.get_screenshot_as_file("D://kw.png")
        #     time.sleep(2)
        #     driver.close(self)
        #
        # # 百度更多-图片 用例
        # def test_more_image(self):
        #     """百度更多中图片链接测试"""
        #     driver = self.driver
        #     # 进入百度更多页
        #     driver.get(self.base_url + "/more/")
        #     # 记录当前窗口handle
        #     handle_index = driver.current_window_handle
        #     # 点击图片链接
        #     element = driver.find_element_by_link_text("图片")
        #     element.click(self)
        #     time.sleep(2)
        #     # 跳转到新开窗口
        #     for handle in driver.window_handles:
        #         if handle != handle_index:
        #             driver.switch_to.window(handle)
        #     self.assertEqual("http://image.baidu.com/", driver.current_url)
        #     driver.close(self)
        #-*- coding:utf-8 -*-
    #author : Lenovo
    #date: 2018/5/30
    def register_text(self):
        try:
            browser.get("http://127.0.0.1:5000/1")
            register_btn=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > nav > div > div.navbar-collapse.collapse > ul > li:nth-child(3) > a')))
            register_btn.click(self)
            name=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#name'))).send_keys(register_list['name'])
            email=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#email'))).send_keys(register_list['email'])
            phone=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#phone'))).send_keys(register_list['phone'])
            pwd=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#pwd'))).send_keys(register_list['pwd'])
            pwd_again=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#pwd_again'))).send_keys(register_list['pwd_again'])
            submit=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#submit')))
            submit.click(self)
            if browser.find_elements_by_css_selector('#input_user'):
                err_list=browser.find_elements_by_css_selector('#input_user')
                for i,err in enumerate(err_list):
                    err_info={u'注册错误信息%s:'%i:err.text}
                    register_list.update(err_info)

                return None
            suc_info={
                'name':register_list['name'],
                'email':register_list['email'],
                'phone':register_list['phone'],
                'pwd':register_list['pwd'],
                'pwd_again':register_list['pwd_again'],
                'status:':u'注册成功'}

        except TimeoutException:
           pass

    def login_text(name,pwd):              #会员登陆测试
        try:
            name_input=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#name')))
            pwd_input=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#pwd')))
            name_input.send_keys(name)
            pwd_input.send_keys(pwd)
            login=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#submit')))
            login.click()
            if browser.find_elements_by_css_selector('#input_user'):
                err_list=browser.find_elements_by_css_selector('#input_user')
                for i,err in enumerate(err_list):
                    err_info={
                        'name':name,
                        'pwd':pwd,
                        u'登陆错误信息%s:'%i:err.text}

            suc_info={
                'name':register_list['name'],
                'pwd':register_list['email'],
                'status:':u'登陆成功'}

        except TimeoutException:
            pass

    def change_info_text(name,email,phone,info):              #修改个人信息测试
        try:
            # name_input=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#name')))
            # name_input.clear(self)
            # name_input.send_keys(name)
            # email_input=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#email')))
            # email_input.clear(self)
            # email_input.send_keys(email)
            # phone_input=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#phone')))
            # phone_input.clear(self)
            # phone_input.send_keys(phone)
            info_input=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#info')))
            info_input.clear()
            info_input.send_keys(info)
            change_btn=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#submit')))
            change_btn.click()
            if browser.find_elements_by_css_selector('#input_user'):
                err_list=browser.find_elements_by_css_selector('#input_user')
                for i,err in enumerate(err_list):
                    err_info={
                        'name':name,
                        'pwd':email,
                        'phone':phone,
                        'info':info,
                         u'修改个人错误信息%s:'%i:err.text}

            suc_info={
                'name':name,
                'email':email,
                'phone':phone,
                'info':info,
                 u'status:':u'修改个人信息成功'}

        except TimeoutException:
            pass


    def change_pwd_text(name,old_pwd,new_pwd,new_pwd_again):              #修改密码测试
        try:
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#me2'))).click(self)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#old_pwd'))).send_keys(old_pwd)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#new_pwd'))).send_keys(new_pwd)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#new_pwd_again'))).send_keys(new_pwd_again)
            change_btn=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#submit')))
            change_btn.click()
            if browser.find_elements_by_css_selector('#input_user'):
                err_list=browser.find_elements_by_css_selector('#input_user')
                for i,err in enumerate(err_list):
                    err_info={
                        'name':name,
                        'old_pwd':old_pwd,
                        'new_pwd':new_pwd,
                        'new_pwd_again':new_pwd_again,
                        u'修改密码信息%s:'%i:err.text}

            suc_info={
                'name':name,
                'old_pwd':old_pwd,
                'new_pwd':new_pwd,
                'new_pwd_again':new_pwd_again,
                'status:':u'修改密码成功'}

            # login_text(register_list['name'],new_pwd)
        except TimeoutException:
            pass


    def search_movie_text(key):              #搜索电影测试
        try:
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#key'))).send_keys(key)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#search'))).click()

            if browser.find_elements_by_css_selector('body > div > div > div.row > div:nth-child(2)'):
                suc_info={
                    'status:':u'搜索电影成功'}

            info={ 'status:':u'没有电影被搜到'}
        except TimeoutException:
            pass


    def admin_login_text(name,pwd):              #管理员登陆测试
        try:
            browser.get("http://127.0.0.1:5000/admin")
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#account'))).send_keys(name)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#pwd'))).send_keys(pwd)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#submit'))).click(self)

            if browser.find_elements_by_css_selector('#input_user'):
                err_list=browser.find_elements_by_css_selector('#input_user')
                for i,err in enumerate(err_list):
                    err_info={
                        'name':name,
                        'old_pwd':pwd,
                        u'管理员登陆错误%s:'%i:err.text}

            suc_info={
                'name':name,
                'pwd':pwd,
                'status:':u'管理员登陆成功'}

        except TimeoutException:
            pass
    def add_tag_text(tag_name):              #添加标签测试
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div > aside > section > ul > li:nth-child(3) > a'))).click(self)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div > aside > section > ul > li.treeview.active > ul > li:nth-child(1) > a'))).click(self)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#input_name'))).send_keys(tag_name)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#submit'))).click(self)
            if browser.find_elements_by_css_selector('#showcontent > div > div > div > form > div.box-body > div.alert-error.alert'):
                    err_info={
                    'name':tag_name,
                    'reason:':u'该标签已经存在'}

            if browser.find_elements_by_css_selector('#showcontent > div > div > div > form > div.box-body > div.alert.alert-success'):
                suc_info={
                    'name':tag_name,
                    'reason:':u'添加标签成功'}

        except TimeoutException:
           pass

    def edit_tag_text(tag_name):              #编辑标签测试
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div > aside > section > ul > li:nth-child(3) > a'))).click(self)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div.wrapper > aside > section > ul > li.treeview.active > ul > li:nth-child(2) > a'))).click(self)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#showcontent > div > div > div > div.box-body.table-responsive.no-padding > table > tbody > tr:nth-child(2) > td:nth-child(4) > a.label.label-success'))).click(self)
            tag=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#input_name')))
            tag.clear()
            tag.send_keys(tag_name)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#submit'))).click(self)
            if browser.find_elements_by_css_selector('#showcontent > div > div > div > div.box-body.table-responsive.no-padding > div'):
                    err_info={
                    'name':tag_name,
                    'reason:':u'该标签已经存在'}

            if browser.find_elements_by_css_selector('#showcontent > div > div > div > div.box-body.table-responsive.no-padding > div'):
                suc_info={
                    'name':tag_name,
                    'reason:':u'修改标签成功'}

        except TimeoutException:
            pass

    def del_tag_text(tag_name):              #删除标签测试
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div > aside > section > ul > li:nth-child(3) > a'))).click(self)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div.wrapper > aside > section > ul > li.treeview.active > ul > li:nth-child(2) > a'))).click(self)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#showcontent > div > div > div > div.box-body.table-responsive.no-padding > table > tbody > tr:nth-child(2) > td:nth-child(4) > a.label.label-danger'))).click(self)
            if browser.find_elements_by_css_selector('#showcontent > div > div > div > div.box-body.table-responsive.no-padding > div'):
                suc_info={
                    'name':tag_name,
                    'reason:':u'删除标签成功'}

        except TimeoutException:
            pass

    def add_movie_text(title,url,info,logo,area,length,addtime):              #添加电影测试
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div > aside > section > ul > li:nth-child(4) > a'))).click(self)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div > aside > section > ul > li.treeview.active > ul > li:nth-child(1) > a'))).click(self)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#input_title'))).send_keys(title)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#url'))).send_keys(url)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#info'))).send_keys(info)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#logo'))).send_keys(logo)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#area'))).send_keys(area)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#length'))).send_keys(length)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#input_release_time'))).send_keys(addtime)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#submit'))).click(self)
            if browser.find_elements_by_css_selector('#showcontent > div > div > div > form > div.box-body > div.alert-error.alert'):
                    err_info={
                    'name':tag_name,
                    'reason:':u'该电影已经存在'}

            if browser.find_elements_by_css_selector('#showcontent > div > div > div > form > div.alert.alert-success'):
                suc_info={
                    'name':tag_name,
                    'reason:':u'添加电影成功'}

        except TimeoutException:
            pass

    def edit_movie_text(title,url,info,logo,area,length,addtime):              #编辑电影测试
         try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div > aside > section > ul > li:nth-child(4) > a'))).click(self)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div > aside > section > ul > li.treeview.active > ul > li:nth-child(2)'))).click(self)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#showcontent > div > div > div > div.box-body.table-responsive.no-padding > table > tbody > tr:nth-child(2) > td:nth-child(10) > a.label.label-success'))).click(self)
            title_edit=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#input_title')))
            title_edit.clear()
            title_edit.send_keys(title)
            url_edit=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#url')))
            url_edit.send_keys(url)
            info_edit= wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#info')))
            info_edit.clear()
            info_edit.send_keys(info)
            logo_edit=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#logo')))
            logo_edit.send_keys(logo)
            area_edit=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#area')))
            area_edit.clear()
            area_edit.send_keys(area)
            length_edit=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#length')))
            length_edit.clear()
            length_edit.send_keys(length)
            addtime_edit=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#input_release_time')))
            addtime_edit.clear()
            addtime_edit.send_keys(addtime)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#submit'))).click(self)
            if browser.find_elements_by_css_selector('#showcontent > div > div > div > form > div.box-body > div.alert-error.alert'):
                    err_info={
                    'name':tag_name,
                    'reason:':u'该电影已经存在'}

            if browser.find_elements_by_css_selector('#showcontent > div > div > div > div.box-header > div.alert.alert-success > h4 > i'):
                suc_info={
                    'name':tag_name,
                    'reason:':u'编辑电影成功'}

         except  TimeoutException:
                pass

    def del_movie_text(self):              #删除电影测试
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div > aside > section > ul > li:nth-child(4) > a'))).click(self)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div > aside > section > ul > li.treeview.active > ul > li:nth-child(2)'))).click(self)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#showcontent > div > div > div > div.box-body.table-responsive.no-padding > table > tbody > tr:nth-child(2) > td:nth-child(10) > a.label.label-danger'))).click(self)
            if browser.find_elements_by_css_selector('#showcontent > div > div > div > form > div.box-body > div.alert-error.alert'):
                    err_info={
                    'reason:':u'删除电影失败'}

            if browser.find_elements_by_css_selector('#showcontent > div > div > div > div.box-header > div.alert.alert-success'):
                suc_info={
                    'reason:':u'删除电影成功'}

        except TimeoutException:
            pass


    def add_preview_text(title,url):              #添加预告测试
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div > aside > section > ul > li:nth-child(5) > a'))).click(self)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div > aside > section > ul > li.treeview.active > ul > li:nth-child(1) > a'))).click(self)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#input_title'))).send_keys(title)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#url'))).send_keys(url)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#submit'))).click(self)
            if browser.find_elements_by_css_selector('#showcontent > div > div > div > form > div.alert-error.alert'):
                    err_info={
                    'name':tag_name,
                    'reason:':u'预告名称重复'}

            if browser.find_elements_by_css_selector('#showcontent > div > div > div > form > div.alert.alert-success'):
                suc_info={
                    'name':tag_name,
                    'reason:':u'添加预告成功'}

        except TimeoutException:
            pass

    def edit_preview_text(title,url):              #编辑预告测试
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div > aside > section > ul > li:nth-child(5) > a'))).click(self)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div > aside > section > ul > li.treeview.active > ul > li:nth-child(2) > a'))).click(self)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#showcontent > div > div > div > div.box-body.table-responsive.no-padding > table > tbody > tr:nth-child(2) > td:nth-child(5) > a.label.label-success'))).click(self)
            input_title=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#input_title')))
            input_title.clear()
            input_title.send_keys(title)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#url'))).send_keys(url)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#submit'))).click(self)
            if browser.find_elements_by_css_selector('#showcontent > div > div > div > form > div.alert-error.alert'):
                    err_info={
                    'name':tag_name,
                    'reason:':u'预告名称重复'}

            if browser.find_elements_by_css_selector('#showcontent > div > div > div > form > div.alert.alert-success'):
                suc_info={
                    'name':tag_name,
                    'reason:':u'编辑预告成功'}

        except TimeoutException:
            pass


    def del_preview_text(self):              #删除预告测试
        try:
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div > aside > section > ul > li:nth-child(5) > a'))).click(self)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div > aside > section > ul > li.treeview.active > ul > li:nth-child(2) > a'))).click(self)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#showcontent > div > div > div > div.box-body.table-responsive.no-padding > table > tbody > tr:nth-child(2) > td:nth-child(5) > a.label.label-danger'))).click(self)
            if browser.find_elements_by_css_selector('#showcontent > div > div > div > div.alert.alert-errors'):
                    err_info={
                    'name':tag_name,
                    'reason:':u'删除预告失败'}

            if browser.find_elements_by_css_selector('#showcontent > div > div > div > div.alert.alert-success'):
                suc_info={
                    'name':tag_name,
                    'reason:':u'删除预告成功'}

        except TimeoutException:
            pass

    def del_user_text(self):              #删除会员测试
        try:
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div > aside > section > ul > li:nth-child(6) > a'))).click(self)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div > aside > section > ul > li.treeview.active > ul > li > a'))).click(self)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#showcontent > div > div > div > div.box-body.table-responsive.no-padding > table > tbody > tr:nth-child(2) > td:nth-child(7) > a.label.label-danger'))).click(self)
            if browser.find_elements_by_css_selector('#showcontent > div > div > div > div.alert.alert-errors'):
                    err_info={
                    'name':tag_name,
                    'reason:':u'删除会员失败'}

            if browser.find_elements_by_css_selector('#showcontent > div > div > div > div.alert.alert-success'):
                suc_info={
                    'name':tag_name,
                    'reason:':u'删除会员成功'}

        except TimeoutException:
            pass
    def add_auth_text(title,url):              #添加权限测试
        try:
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div > aside > section > ul > li:nth-child(10) > a > span:nth-child(2)'))).click(self)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div > aside > section > ul > li.treeview.active > ul > li:nth-child(1) > a'))).click(self)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#showcontent > div > div > div > form > div.box-body > div:nth-child(1) #input_title'))).send_keys(title)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#showcontent > div > div > div > form > div.box-body > div:nth-child(2) #input_title'))).send_keys(url)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#submit'))).click(self)
            if browser.find_elements_by_css_selector('#showcontent > div > div > div > div.alert.alert-error'):
                    err_info={
                    'name':tag_name,
                    'reason:':u'权限名称重复'}

            if browser.find_elements_by_css_selector('#showcontent > div > div > div > div.alert.alert-success'):
                suc_info={
                    'name':tag_name,
                    'reason:':u'添加权限成功'}

        except TimeoutException:
            pass

    def edit_auth_text(title,url):              #编辑权限测试
        try:
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div > aside > section > ul > li:nth-child(10) > a > span:nth-child(2)'))).click(self)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div > aside > section > ul > li.treeview.active > ul > li:nth-child(2) > a'))).click(self)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#showcontent > div > div > div > div.box-body.table-responsive.no-padding > table > tbody > tr:nth-child(2) > td:nth-child(5) > a.label.label-success'))).send_keys(title)
            auth_title=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#showcontent > div > div > div > form > div.box-body > div:nth-child(1) #input_title')))
            auth_title.clear()
            auth_title.send_keys(title)
            auth_url=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#showcontent > div > div > div > form > div.box-body > div:nth-child(2) #input_title')))
            auth_url.clear()
            auth_url.send_keys(url)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#submit'))).click(self)
            if browser.find_elements_by_css_selector('#showcontent > div > div > div > div.alert.alert-error'):
                    err_info={
                    'name':title,
                    'reason:':u'权限名称重复'}

            if browser.find_elements_by_css_selector('#showcontent > div > div > div > div.alert.alert-success'):
                suc_info={
                    'name':title,
                    'reason:':u'编辑权限成功'}

        except TimeoutException:
           pass

    def del_auth_text(self):              #删除权限测试
        try:
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div > aside > section > ul > li:nth-child(10) > a > span:nth-child(2)'))).click(self)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div > aside > section > ul > li.treeview.active > ul > li:nth-child(2) > a'))).click(self)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#showcontent > div > div > div > div.box-body.table-responsive.no-padding > table > tbody > tr:nth-child(2) > td:nth-child(5) > a.label.label-danger'))).click(self)
            if browser.find_elements_by_css_selector('#showcontent > div > div > div > form > div.alert-error.alert'):
                    err_info={
                    'name':tag_name,
                    'reason:':u'删除权限失败'}

            if browser.find_elements_by_css_selector('#showcontent > div > div > div > div.alert.alert-success'):
                suc_info={
                    'name':tag_name,
                    'reason:':u'删除权限成功'}

        except TimeoutException:
            pass

    def add_role_text(title):              #添加角色测试
        try:
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'li.treeview:nth-child(11) > a:nth-child(1) > span:nth-child(2)'))).click(self)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div > aside > section > ul > li.treeview.active > ul > li:nth-child(1) > a'))).click(self)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#input_title'))).send_keys(title)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#input_title > option:nth-child(2)'))).click(self)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#submit'))).click(self)
            if browser.find_elements_by_css_selector('#showcontent > div > div > div > div.alert.alert-error'):
                    err_info={
                    'name':tag_name,
                    'reason:':u'角色名称重复'}

            if browser.find_elements_by_css_selector('#showcontent > div > div > div > div.alert.alert-success'):
                suc_info={
                    'name':tag_name,
                    'reason:':u'添加角色成功'}

        except TimeoutException:
            pass

    def edit_role_text(title):              #编辑角色测试
        try:
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'li.treeview:nth-child(11) > a:nth-child(1) > span:nth-child(2)'))).click(self)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div > aside > section > ul > li.treeview.active > ul > li:nth-child(2) > a'))).click(self)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#showcontent > div > div > div > div.box-body.table-responsive.no-padding > table > tbody > tr:nth-child(5) > td:nth-child(5) > a.label.label-success'))).click(self)
            role_name=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#input_title')))
            role_name.clear()
            role_name.send_keys(title)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#input_title > option:nth-child(2)'))).click(self)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#submit'))).click(self)
            if browser.find_elements_by_css_selector('#showcontent > div > div > div > div.alert.alert-error'):
                    err_info={
                    'name':tag_name,
                    'reason:':u'角色名称重复'}

            if browser.find_elements_by_css_selector('#showcontent > div > div > div > div.alert.alert-success'):
                suc_info={
                    'name':tag_name,
                    'reason:':u'编辑角色成功'}

        except TimeoutException:
            pass

    def del_role_text(self):              #删除角色测试
        try:
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div > aside > section > ul > li:nth-child(11) > a'))).click(self)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div > aside > section > ul > li.treeview.active > ul > li:nth-child(2) > a'))).click(self)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#showcontent > div > div > div > div.box-body.table-responsive.no-padding > table > tbody > tr:nth-child(6) > td:nth-child(5) > a.label.label-danger'))).click(self)
            if browser.find_elements_by_css_selector('#showcontent > div > div > div > div.alert.alert-eror'):
                    err_info={
                    'name':tag_name,
                    'reason:':u'删除角色失败'}

            if browser.find_elements_by_css_selector('#showcontent > div > div > div > div.alert.alert-success'):
                suc_info={
                    'name':tag_name,
                    'reason:':u'删除角色成功'}

        except TimeoutException:
            pass


    # def write_to_file(content):
    #     with open('movie_text.txt','a') as f:
    #         text=json.dumps(content,ensure_ascii=False)
    #         text=unicode.encode(text,'utf-8')
    #         f.write(text+'\n')
    #
    # def main(self):
    #     while True:
    #         print(u'--------------------微电影网站测试--------------------------')
    #         print(u'===================请选择测试选项============================')
    #         print(u'1.会员注册  2.会员登陆  3.会员修改个人信息  4.会员修改密码')
    #         print('-----------------------------------------------------------')
    #         print(u'6.添加标签  7.编辑标签  8.添加电影')
    #         print('------------------------------------------------------------')
    #         print(u'9.编辑电影  10.删除电影 11.添加预告 12.编辑预告')
    #         print('-------------------------------------------------------------')
    #         print(u'13.删除预告 14.添加角色 15.编辑角色 16.删除角色')
    #         print('--------------------------------------------------------------')
    #         print(u'17.添加权限 18.编辑权限  19.删除权限')
    #         choice=raw_input(u'请输入选项')
    #         if choice=='1':
    #             register_text(self)                  #注册测试
    #         if choice=='2':
    #             login_text(register_list['name'],register_list['pwd'])       #登陆测试
    #         if choice=='3':
    #             change_info_text(change_info['name'],change_info['email'],change_info['phone'],change_info['info'])          #修改个人信息测试
    #         if choice=='4':
    #              change_pwd_text(change_pwd['name'],change_pwd['old_pwd'],change_pwd['new_pwd'],change_pwd['new_pwd_again'])      #修改密码测试
    #         if choice=='6':
    #             admin_login_text(admin_login_ingo['name'],admin_login_ingo['pwd'])                   #管理员登陆
    #             add_tag_text(tag_name['name'])                  #添加标签测试
    #         if choice=='7':
    #             admin_login_text(admin_login_ingo['name'],admin_login_ingo['pwd'])                   #管理员登陆
    #             edit_tag_text(tag_name['name'])                 #编辑标签测试
    #         if choice=='8':
    #             admin_login_text(admin_login_ingo['name'],admin_login_ingo['pwd'])                   #管理员登陆
    #             del_tag_text(tag_name['name'])                  #删除标签测试
    #         if choice=='9':
    #             admin_login_text(admin_login_ingo['name'],admin_login_ingo['pwd'])                   #管理员登陆
    #             add_movie_text(movie_add_info['title'],movie_add_info['url'],movie_add_info['info'],movie_add_info['logo'],movie_add_info['area'],movie_add_info['lenth'],movie_add_info['addtime'],)
    #         if choice=='10':
    #             admin_login_text(admin_login_ingo['name'],admin_login_ingo['pwd'])                   #管理员登陆
    #             edit_movie_text(movie_edit_info['title'],movie_edit_info['url'],movie_edit_info['info'],movie_edit_info['logo'],movie_edit_info['area'],movie_edit_info['lenth'],movie_edit_info['addtime'],)
    #         if choice=='11':
    #             admin_login_text(admin_login_ingo['name'],admin_login_ingo['pwd'])                   #管理员登陆
    #             del_movie_text(self)     #删除电影测试
    #         if choice=='12':
    #             admin_login_text(admin_login_ingo['name'],admin_login_ingo['pwd'])                   #管理员登陆
    #             add_preview_text(u'韩剧','C:\\Users\\Lenovo\\Desktop\\big0720150102210934.jpg')      #增加预告测试
    #         if choice=='13':
    #             admin_login_text(admin_login_ingo['name'],admin_login_ingo['pwd'])                   #管理员登陆
    #             edit_preview_text(u'美剧','C:\\Users\\Lenovo\\Desktop\\big0720150102210934.jpg')        #编辑预告测试
    #         if choice=='14':
    #             admin_login_text(admin_login_ingo['name'],admin_login_ingo['pwd'])                   #管理员登陆
    #             del_preview_text(self)                                                                            #删除预告测试
    #         if choice=='15':
    #             admin_login_text(admin_login_ingo['name'],admin_login_ingo['pwd'])                   #管理员登陆
    #             add_role_text(u'普通角色')          #增加角色测试
    #         if choice=='16':
    #             admin_login_text(admin_login_ingo['name'],admin_login_ingo['pwd'])                   #管理员登陆
    #             edit_role_text(u'正常角色')         #编辑角色测试
    #         if choice=='17':
    #             admin_login_text(admin_login_ingo['name'],admin_login_ingo['pwd'])                   #管理员登陆
    #             del_role_text(self)                     #删除角色测试
    #         if choice=='18':
    #             admin_login_text(admin_login_ingo['name'],admin_login_ingo['pwd'])                   #管理员登陆
    #             add_auth_text(u'增加管理员','admin/del_admin')        #增加权限测试
    #         if choice=='19':
    #             admin_login_text(admin_login_ingo['name'],admin_login_ingo['pwd'])                   #管理员登陆
    #             edit_auth_text(u'编辑管理员','admin/del_admin')       #编辑权限测试
    #


# if __name__=="__main__":
#     main(self)
#     # import Tkinter
#     # from Tkinter import *
#     # root = Tkinter.Tk(self)
#     # # 进入消息循环
#     # root.title('微电影测试')
#     # root.geometry('300x200')
#     # l = Label(root, text="show", bg="green", font=("Arial", 12), width=5, height=2)
#     # l.pack(side=LEFT)
#     # root.mainloop(self)

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == '__main__':
    unittest.main()