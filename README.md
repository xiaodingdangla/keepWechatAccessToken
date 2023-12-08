<img src="42042015.jpg" align="right" />

# 微信公众号AccessToken保活  [![Awesome](badge.svg)](#)
> Get the AccessToken of WeChat official account regularly

## 项目介绍
本项目基于python3.12 框架为APScheduler和FastAPI
通过定时任务获取微信公众号的AccessToken,然后将AccessToken存入redis中
通过FastAPI提供接口，供其他项目调用