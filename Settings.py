#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Zhenyu Chan
# E-mail:hsczyic@gmail.com
# Time: : 2020/6/15 4:32 下午
import os

FileDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'FileDir')
if not os.path.exists(FileDir):
    os.mkdir(FileDir)
BaseDir = os.path.dirname(os.path.abspath(__file__))

