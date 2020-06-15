#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Zhenyu Chan
# E-mail:hsczyic@gmail.com
# Time: : 2020/6/15 8:35 下午
import os

from fastapi.testclient import TestClient
from main import api

client = TestClient(api)
dir_name = os.path.join(os.path.dirname(os.path.abspath(__file__)),'TestFile')


def test_post_image():
    image_file = os.path.join(dir_name, 'test.png')
    resp = client.post("/uploadImage", files={'file': ('test.png', open(image_file, 'rb'), 'image/png')})
    assert resp.status_code == 200
    assert resp.json()['content'] == ["N", "o", "i", "s", "y", "i", "m", "a", "g", "e", "t", "o", "t", "e", "s", "t",
                                      "T", "e", "s", "s", "e", "r", "a", "c", "t", "O", "C", "R"]


def test_post_txt():
    image_file = os.path.join(dir_name, 'test.txt')
    resp = client.post("/uploadImage", files={'file': ('test.txt', open(image_file, 'rb'))})
    assert resp.status_code == 501
    assert resp.json()['msg'] == '类型错误，只能接受图片类型(image)文件。'


if __name__ == '__main__':
    test_post_image()
    test_post_txt()
