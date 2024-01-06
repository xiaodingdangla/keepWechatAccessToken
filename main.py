import json
import logging

import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from scheduler import scheduler, load_config_from_env
from connection_pool import Connect
config = load_config_from_env()

logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
fh = logging.FileHandler(filename=config['log_path'])
formatter = logging.Formatter(
    "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"
)
fh.setFormatter(formatter)
# 将日志输出至文件,编码为utf-8
fh.encoding = 'utf-8'
logger.addHandler(fh)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info('开始启动')
    with Connect() as db:
        db.cur.execute("CREATE TABLE IF NOT EXISTS key_value (kk TEXT PRIMARY KEY, vv TEXT)")
        db.conn.commit()
    scheduler.start()
    yield
    logging.info('开始关闭')
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)


# 通过路由获取access_token
@app.get("/wechat/access_token", tags=["wechat"], summary="获取access_token")
async def get_access_token():
    with Connect() as db:
        db.cur.execute("SELECT * FROM key_value WHERE kk = 'wechat_configurations'")
        result = db.cur.fetchone()
    return json.loads(result[1])


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
