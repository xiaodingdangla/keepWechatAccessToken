<img src="dingdang.jpg" align="right" />

# 微信公众号AccessToken保活  [![Awesome](badge.svg)](#)
> Get the AccessToken of WeChat official account regularly

## 项目介绍:
这是一个基于 Python 3.x 的定时任务服务，定期获取微信公众号的 AccessToken，并安全地存储在 SQLite 数据库中。项目使用 APScheduler 和 FastAPI 框架，实现任务调度和提供安全接口服务。

### 主要功能:
- 定时任务管理: 使用 APScheduler 定期获取微信公众号 AccessToken，确保保持最新状态。
- 数据存储: 将 AccessToken 安全存储在 SQLite 数据库中，为其他项目提供可靠的访问和使用。
- 接口服务: 使用 FastAPI 提供安全接口，其他项目可通过 API 获取最新的 AccessToken，异步特性确保高性能。
- 配置管理: 用户通过配置 .env 文件参数，简便地配置微信公众号信息和其他项目参数。
- 安全性: 禁止对外暴露 API 接口，通过配置文件参数方式进行部署，确保系统稳定和安全。

### 部署建议:
为了确保项目的正常运行和安全性，建议部署时不对外暴露 API 接口。用户只需在 .env 文件中配置相关参数，即可简便地运行该项目。该设计方案降低了部署的复杂性，使得项目在不同环境中都能轻松部署和运行。

## 部署简易流程

### 环境要求:
- Python 3.x
- FastAPI
- APScheduler
- requests
- Gunicorn

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

### 配置文件
```bash
# .env
WECHAT_APPID = xxxxx
WECHAT_SECRET = xxxxx
WECHAT_API_URL= xxxxx
LOG_PATH = /path/to/log
```