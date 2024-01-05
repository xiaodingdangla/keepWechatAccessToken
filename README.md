<img src="42042015.jpg" align="right" />

# 微信公众号AccessToken保活  [![Awesome](badge.svg)](#)
> Get the AccessToken of WeChat official account regularly

## 项目介绍
该项目是一个基于python 3.x的定时任务项目，使用了APScheduler和FastAPI框架。主要功能是通过定时任务获取微信公众号的AccessToken，并将其存入Redis中。同时，通过FastAPI提供接口，供其他项目调用。为了保障安全，部署本项目时请勿对外暴露API接口。只需配置.env文件中的参数，即可运行该项目。

## 环境要求
- python3.x
- redis
- FastAPI（用于提供接口）
- APScheduler（用于定时任务）
- requests
- gunicorn

## 部署
### 本地部署
```bash
# 安装依赖
pip install -r requirements.txt
# 启动项目
python main.py
```
### docker部署
```bash
# 构建镜像
docker build -t dang-token:1.0.2 .
# 启动容器
docker run -d --name dang-token -p 8000:8000 dang-token:1.0.2
```

## 配置文件
```bash
# .env
# 微信公众号AppID
WECHAT_APPID = xxxxx
# 微信公众号SECRET
WECHAT_SECRET = xxxxx
# redis地址
REDIS_HOST = xxxxx
# redis端口
REDIS_PORT = 6379
# redis密码
REDIS_PASSWORD = xxxxx
# redis库
REDIS_DB = 0
# 日志路径
LOG_PATH = /path/to/log
```