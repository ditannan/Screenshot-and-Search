# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 22:25:34 2018

@author: xzm
"""

import win32gui
import win32ui
import win32con
import win32api

import requests
from PIL import Image
from aip import AipOcr
from io import BytesIO
import os
import webbrowser
import jieba
import jieba.analyse
import time
import subprocess


def cap(filename):
#    filename = 'new_new.jpg'
    hwnd = 0
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    w = 500
    h = 500
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)
    
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (-520, 75), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)
    
    
    new_new = Image.open('new_new.jpg')
    imgByteArr = BytesIO()
    new_new.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()    
    return imgByteArr

cap('aaaa.jpg')  

def get_word_by_img(img):
    """文字提取"""
    APP_ID = '10704639'
    API_KEY = 'W19KOxuw4ic6ZAC21pRmSD3R'
    SECRET_KEY = 'GnGBt44E5LdE18kSNKN4h6ROxhsCmnFR'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    res = client.basicGeneral(img)
    return res

def baidu(question, answers):
    """搜索答案"""
    url = 'https://www.baidu.com/s'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    data = {
        'wd': question
    }
    res = requests.get(url, params=data, headers=headers)
    res.encoding = 'utf-8'
    html = res.text
    # 分析
    
    for i in range(len(answers)):
        answers[i] = (html.count(answers[i]), answers[i], i+1)
    answers.sort(reverse=True)
    return answers


def run():
    """主函数"""
    mess = '请输入回车开始答题：'
    mess += "\n输入'quit' 结束答题.\n"
    message = ''
    active = True
    while active:
        message = input(mess)
        if message == 'quit':
            break
        
#        t1 = time.time()
        
        # 获取手机截图
        img = cap('new_new.jpg')
        
 #       t2 = time.time()
        
 #       print(t2 - t1)
        # 提取文字
        info = get_word_by_img(img)
        

        
        # 提取答案和问题
        answers = [x['words'] for x in info['words_result'][-3:]]
        ans1 = answers[0][:]
        ans2 = answers[1][:]
        ans3 = answers[2][:]
        
        question = ''.join([x['words'] for x in info['words_result'][:-3]])
        question = question[1:]
        
        # 根据题目搜索
        res = baidu(question, answers)
        print(question, '\n')
        print(res, '\n')  
        
 #       t3 = time.time()
 #       print(t3 - t2)
        
 #       title_cut = jieba.analyse.extract_tags(question, topK=4)
 #       for i in range(len(answers)):
  #          html = baidudu(answers[i][1])
  #          title_num = {}
  #          for j in range(len(title_cut)):
   #             title_num[j] = (title_cut[j], html.count(title_cut[j]))
   #         print(answers[i][1], title_num, '\n') 
        
  #      t4 = time.time()
  #      print(t4 - t3)
        
        url1 = 'http://www.baidu.com/s?wd=%s' %ans1
        webbrowser.open(url1, new=2)
        url2 = 'http://www.baidu.com/s?wd=%s' %ans2
        webbrowser.open(url2, new=2)
        url3 = 'http://www.baidu.com/s?wd=%s' %ans3
        webbrowser.open(url3, new=2)
        url = 'http://www.baidu.com/s?wd=%s' %question
        webbrowser.open(url, new=2)
        
  #      t5 = time.time()
 #       print(t5 - t4)
  #      print(t5 - t1)


run()



