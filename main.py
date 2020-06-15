#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Zhenyu Chan
# E-mail:hsczyic@gmail.com
# Time: : 2020/6/15 4:06 下午
import os

import uvicorn
from fastapi import FastAPI, UploadFile, File
from starlette.responses import JSONResponse

from Modules.OCR.OCRBaidu import OCRBaidu
from Modules.OCR.OCRLocal import OCRLocal
from Settings import FileDir
from Utils.Snowflake import SnowFlake

from Static.StatusCode import StatusCode, error_map

api = FastAPI()


@api.post('/uploadImage')
async def uploadImage(file: UploadFile = File(...)):
    if 'image' in file.content_type:

        # 为图片重新命名
        file_name = f"{'.'.join(file.filename.split('.')[:-1])}_{SnowFlake(1, 1).make_snowflake()}" \
                    f".{file.filename.split('.')[-1]}"
        # 读取图片内容并保存至本地文件
        content = await file.read()
        with open(os.path.join(FileDir, file_name), 'wb') as f:
            f.write(content)
        # OCR对图片进行OCR扫描
        try:
            # 首先使用本地进行测试
            litters_list = OCRLocal(file_name).get_litter()
        except:
            litters_list = OCRBaidu(file_name).get_litter()
        return JSONResponse(status_code=StatusCode.OK, content={'content': litters_list})
    else:
        return JSONResponse(status_code=StatusCode.TypeError, content={'msg': error_map.get(StatusCode.TypeError)})


if __name__ == '__main__':
    uvicorn.run(api)
