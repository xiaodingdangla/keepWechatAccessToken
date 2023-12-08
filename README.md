<img src="42042015.jpg" align="right" />

# 微信公众号AccessToken保活  [![Awesome](badge.svg)](#)
> Get the AccessToken of WeChat official account regularly

## 项目介绍
本项目基于python3.x 框架为APScheduler和FastAPI
通过定时任务获取微信公众号的AccessToken，然后将AccessToken存入redis中。
通过FastAPI提供接口，供其他项目调用，部署本项目请勿对外暴露API接口。
配置.env文件中的参数,即可运行。

## 环境要求
- python3.x
- redis
- FastAPI
- APScheduler
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
docker build -t keep_token:v1.0 .
# 启动容器
docker run -d --name keep_token -p 8000:8000 keep_token:v1.0
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
# redis用户
REDIS_USER = xxxxx
# redis密码
REDIS_PASSWORD = xxxxx
# redis库
REDIS_DB = 0
