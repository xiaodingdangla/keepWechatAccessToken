import json
import logging
import os, requests
import urllib.parse
from connection_pool import Connect
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv(find_dotenv('.env'))
env_dist = os.environ


def load_config_from_env():
    load_dotenv(find_dotenv('.env'))
    env_dist = os.environ
    return {
        "wechat_appid": env_dist.get('WECHAT_APPID'),
        "wechat_secret": env_dist.get('WECHAT_SECRET'),
        "wechat_api_url": env_dist.get('WECHAT_API_URL'),
        "log_path": env_dist.get('LOG_PATH'),
    }


config = load_config_from_env()


def get_access_token():
    try:
        kw = {"grant_type": "client_credential", "appid": config['wechat_appid'], "secret": config['wechat_secret']}
        # 发送请求
        url = urllib.parse.urljoin(config['wechat_api_url'], "/cgi-bin/token")
        res = requests.get(url, params=kw, timeout=10)

        res.raise_for_status()  # 检查请求是否成功，如果不成功则抛出异常

        wechat_access_token = res.json().get('access_token')
        if wechat_access_token is None:
            # 直接抛出异常
            raise Exception("get access_token fail")

        create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 构造配置信息
        wechat_configurations = {
            "access_token": wechat_access_token,
            "create_time": create_time
        }

        # 转换为JSON字符串
        wechat_json = json.dumps(wechat_configurations)

        # 存入Redis
        with Connect() as db:
            db.cur.execute(f"INSERT OR REPLACE INTO key_value VALUES ('wechat_configurations','{str(wechat_json)}')")
            db.conn.commit()
        logging.info(f"获取 access_token 成功，当前时间: {create_time}")
    except Exception as err:
        logging.error(f"发生错误: {err}")
        with Connect() as db:
            db.cur.execute("select * from key_value where kk = 'retry_count'");
            res = db.cur.fetchone()
            retry_count = int(res[1]) + 1 if res else 1
            logging.info(f"重试次数: {retry_count}")
            if retry_count <= 5:
                db.cur.execute(f"INSERT OR REPLACE INTO key_value VALUES ('retry_count',{retry_count})")
                db.conn.commit()
                get_access_token()
            else:
                logging.error(f"已达到最大重试次数，放弃获取 access_token")
                # 把重试次数清空
                db.cur.execute(f"INSERT OR REPLACE INTO key_value VALUES ('retry_count','0')")
                db.conn.commit()


scheduler = AsyncIOScheduler()

# 添加定时任务
scheduler.add_job(func=get_access_token, trigger='interval', seconds=7100, id='get_access_token',
                  next_run_time=datetime.now())
