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
    # 请求微信服务器
    try:
        kw = {
            "grant_type": "client_credential",
            "appid": wechat_appid,
            "secret": wechat_secret
        }
        # 发送请求
        res = requests.get(f"{wechat_api_url}/cgi-bin/token", params=kw, timeout=10)
    # 捕获异常
    except Exception as e:
        print(f"get access_token error: {e}")
        # 重新请求
        get_access_token()
        return
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


scheduler = AsyncIOScheduler(**interval_task)

# 添加定时任务
scheduler.add_job(func=get_access_token, trigger='interval', seconds=7100, id='get_access_token',next_run_time=datetime.now())
