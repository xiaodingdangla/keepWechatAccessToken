import json
import os, redis, requests
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
        res = requests.get(f"{wechat_api_url}/cgi-bin/token", params=kw, timeout=10)
        res.raise_for_status()  # 检查请求是否成功，如果不成功则抛出异常
        wechat_access_token = res.json().get('access_token')
        create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        wechat_configurations = {
            "access_token": wechat_access_token,
            "create_time": create_time
        }
        # 转换为json
        wechat_json = json.dumps(wechat_configurations)
        # 存入redis
        redis_conn.set("wechat_configurations", str(wechat_json))
        print(f"get access_token success, current time: {create_time}")
    except requests.RequestException as req_err:
        print(f"Request error: {req_err}")
    except json.JSONDecodeError as json_err:
        print(f"JSON decoding error: {json_err}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    else:
        # 如果没有异常，可以执行一些额外的操作
        pass
    finally:
        # 无论是否发生异常，都会执行的代码块
        pass


scheduler = AsyncIOScheduler(**interval_task)

# 添加定时任务
scheduler.add_job(func=get_access_token, trigger='interval', seconds=7100, id='get_access_token',
                  next_run_time=datetime.now())
