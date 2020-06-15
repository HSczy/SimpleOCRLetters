## SimpleOCRLetters

### 环境

Python版本：Python3.8.3

运行环境：macOS

数据库：SQLite3

所运用Python库：opencv、pytesseract、pillow、fastapi、uvicorn、百度云SDK等

其他开源库：tesseract



### 项目运行

1. 将项目克隆到本地
2. 使用`pip install pipenv`命令安装虚拟环境管理工具**pipenv**
3. 在项目根目录下使用命令`pipenv install`安装环境
    - 如果本地电脑没有安装过`tesseract`,使用命令行工具brew进行安装，在命令行中运行命令`brew install tesseract`，进行安装。
4. 在根目录下运行`pytest`进行测试
5. 在根目录下运行`uvicorn main:api --port 8080`命令，开启服务监听本地8080端口，可使用postman等接口测试工具向接口`http://0.0.0.0:8080/uploadImage`使用post方法发送内容获取数据

6. 示例

    1. 请求示例

        method:post

        Url: http://0.0.0.0:8080/uploadImage

        Content-type:image/png

    2. 返回示例

        1. 当发送的数据为image时，接口会对数据进行处理并返回如下内容

            ```json
            {
                "content": [
                    "N",
                    "o",
                    "i",
                    "s",
                    "y",
                    "i",
                    "m",
                    "a",
                    "g",
                    "e",
                    "t",
                    "o",
                    "t",
                    "e",
                    "s",
                    "t",
                    "T",
                    "e",
                    "s",
                    "s",
                    "e",
                    "r",
                    "a",
                    "c",
                    "t",
                    "O",
                    "C",
                    "R"
                ]
            }
            ```

        2. 当发送数据不为image时，接口返回如下：

            ```json
            {
                "msg": "类型错误，只能接受图片类型(image)文件。"
            }
            ```

            

### 项目设计

#### 总体设计

由于项目要求简单只需要编写一个接口即可，故采用轻量框架`FastAPI`编写RestFulAPI接口，同时项目要求有数据本地化存储需求，故采用轻量的关系型数据库SQLite作为后台数据库，由于为展示接口，上传的图片以原有名字+Snowflakes算法的ID拼接的名字存储在本地，方便后续对比、查看、调用。如需部署应使用专门的服务器或oss进行存储、分类。

#### 图像识别模块

图像识别采用两种方式实现，一种使用本地的`Tesseract`进行图片处理，一种使用百度云SDK进行处理。如需使用百度SDK需要提前申请好相对应的appID、APIKey和SecretKey。

#### 数据库模块

数据库采用关系型数据库SQLite3，由于其轻便易于部署故采用。存储记录的表名为“data_parse”,其中具体的键设计如下：

| 字段名       | 类型 | 其他说明                                 |
| ------------ | ---- | ---------------------------------------- |
| id           | int  | 主键、自增长                             |
| file_path    | str  | 记录源文件存储的位置                     |
| created_time | str  | 字符串形式的时间戳，记录图像解析的时间   |
| result       | str  | json类型的列表，记录当前文件分析出的结果 |



### 其他

此项目为demo项目，提供解决思路和方法，其他的细节比如数据库设计、字段的增加、用户的验证、交互的个性化等有考虑但没有来得及做，如有任何问题请联系我。