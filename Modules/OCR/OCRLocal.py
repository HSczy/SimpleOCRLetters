#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Zhenyu Chan
# E-mail:hsczyic@gmail.com
# Time: : 2020/6/15 5:12 下午
import datetime
import json

from PIL import Image
import pytesseract
import cv2
import os

from sqlalchemy.orm import Session

from Modules.OCR import FileDir
from Modules.SQLApp import CRUD
from Modules.SQLApp.Database import SessionLocal
from Modules.SQLApp.Schemas import DataParseCreate


class OCRLocal:
    """
    使用tesseract进行图片OCR处理
    """

    def __init__(self, file_name, preprocess='thresh'):
        self.file_name = os.path.join(FileDir, file_name)
        self.preprocess = preprocess
        self.db: Session = SessionLocal()


    def get_content_from_pic(self):
        # 读取文件
        image = cv2.imread(self.file_name)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 选择不同的模式处理图片
        # 普通模式
        if self.preprocess == "thresh":
            gray = cv2.threshold(gray, 0, 255,
                                 cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # 降噪模式
        elif self.preprocess == 'blur':
            gray = cv2.medianBlur(gray, 3)

        # 将临时文件存在本地然后进行处理识别后删除文件
        filename = os.path.join(FileDir, f"{os.getpid()}.png")
        cv2.imwrite(filename, gray)
        # 获取图片上的文字
        text = pytesseract.image_to_string(Image.open(filename))
        # 删除临时文件
        os.remove(filename)
        return text

    def get_litter(self):
        # 对文本进行处理，返回字母列表
        content = self.get_content_from_pic()
        if ' ' in content:
            content = content.replace(' ', '')
        if '\n' in content:
            content = content.replace('\n', '')
        schema_data = DataParseCreate(
            file_path=self.file_name,
            create_time=datetime.datetime.now().timestamp(),
            result=json.dumps(list(content))
        )
        CRUD.create_data_parse(db=self.db, data=schema_data)
        return list(content)


if __name__ == '__main__':
    print(OCRLocal('97652-150a53012f8e5279.png').get_litter())
