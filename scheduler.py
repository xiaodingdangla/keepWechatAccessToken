import json
import logging
import os, redis, requests
import urllib.parse

from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor

load_dotenv(find_dotenv('.env'))
env_dist = os.environ

# load env
# wechat config
wechat_appid = env_dist.get('WECHAT_APPID')
wechat_secret = env_dist.get('WECHAT_SECRET')
wechat_api_url = env_dist.get('WECHAT_API_URL')
# redis
redis_host = env_dist.get('REDIS_HOST')
redis_port = env_dist.get('REDIS_PORT')
redis_username = env_dist.get('REDIS_USERNAME')
redis_password = env_dist.get('REDIS_PASSWORD')
redis_db = env_dist.get('REDIS_DB')
log_path = env_dist.get('LOG_PATH')

# redis connection
pool = redis.ConnectionPool(host=redis_host, port=redis_port, db=redis_db, username=redis_username,
                            password=redis_password, decode_responses=True)
redis_conn = redis.Redis(connection_pool=pool)

interval_task = {
    "jobstores": {
        "redis": RedisJobStore(host=redis_host, port=redis_port, db=redis_db, username=redis_username,
                               password=redis_password)
    },
    "executors": {
        "default": ThreadPoolExecutor(10)
    },
    "job_defaults": {
        # 任务默认执行器
        "coalesce": False,
        # 最大并发数
        "max_instances": 3
    },
}


def get_access_token():
    try:
        kw = {
            "grant_type": "client_credential",
            "appid": wechat_appid,
            "secret": wechat_secret
        }
        # 发送请求
        url = urllib.parse.urljoin(wechat_api_url, "/cgi-bin/token")
        res = requests.get(url, params=kw, timeout=10)

        res.raise_for_status()  # 检查请求是否成功，如果不成功则抛出异常

        wechat_access_token = res.json().get('access_token')
        create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 构造配置信息
        wechat_configurations = {
            "access_token": wechat_access_token,
            "create_time": create_time
        }

        # 转换为JSON字符串
        wechat_json = json.dumps(wechat_configurations)

        # 存入Redis
        redis_conn.set("wechat_configurations", str(wechat_json))

        logging.info(f"获取 access_token 成功，当前时间: {create_time}")
    except requests.RequestException as req_err:
        logging.error(f"请求错误: {req_err}")
    except json.JSONDecodeError as json_err:
        logging.error(f"JSON 解码错误: {json_err}")
    except Exception as e:
        logging.error(f"意外错误: {e}")


scheduler = AsyncIOScheduler(**interval_task)

# 添加定时任务
scheduler.add_job(func=get_access_token, trigger='interval', seconds=7100, id='get_access_token',
                  next_run_time=datetime.now())
