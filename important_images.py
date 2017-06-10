# encoding: utf-8

import random

_images = [
        'https://upload.wikimedia.org/wikipedia/commons/e/e4/%E4%B8%AD%E8%8F%AF%E6%B0%91%E5%9C%8B%E7%AC%AC12%E3%80%8113%E4%BB%BB%E7%B8%BD%E7%B5%B1%E9%A6%AC%E8%8B%B1%E4%B9%9D%E5%85%88%E7%94%9F%E5%AE%98%E6%96%B9%E8%82%96%E5%83%8F%E7%85%A7.jpg',
        'http://attach.setn.com/newsimages/2015/05/09/263906.jpg',
        'https://c4.staticflickr.com/4/3492/3464131894_00370eb765.jpg',
        'http://img.ltn.com.tw/Upload/talk/page/800/2015/05/18/phpjWgYPG.jpeg'
    ]

def get_image():
    return random.choice(_images)
