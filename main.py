import json

import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from scheduler import scheduler, redis_conn


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('开始启动')
    scheduler.start()
    yield
    print('开始关闭')
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)


# 通过路由获取access_token
@app.get("/wechat/access_token", tags=["wechat"], summary="获取access_token")
async def get_access_token():
    return json.loads(redis_conn.get("wechat_configurations"))


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
