import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils import getJavaServerStatus, schedule_job, get_last_hour_date_info, get_current_day_time_utc8, parse_date_to_h_m_s
from contextlib import asynccontextmanager
from db import MCDB
from pydantic import BaseModel
import aiohttp
from pathlib import Path

class Password(BaseModel):
    code: str

mcdb = MCDB()

with open(Path(__file__).parent.parent / "config.json", encoding="utf-8") as f:
    config = json.load(f)

HOST = config["mc_host"]
PASSWORD = config["password"]
RCON_SERVER = config["rcon_host"]

scheduler = AsyncIOScheduler()
# 每30s记录一次
scheduler.add_job(schedule_job, 'interval', [HOST, mcdb], seconds=30)

origins = [
    "*"
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    mcdb.cursor.close()
    mcdb.conn.close()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    try:
        status = await getJavaServerStatus(HOST)
    except Exception:
        return {
            "time": get_current_day_time_utc8(),
            "description": "请求错误",
            "latency": 10000,
            "max": "请求错误",
            "online": "请求错误"
    }

    return {
        "time": get_current_day_time_utc8(),
        "description": status.description,
        "latency": round(status.latency, 2),
        "max": status.players.max,
        "online": status.players.online
    }

@app.get("/get_latency")
async def get_latency_info():
    # 获取一个小时前的时间
    one_hour_ago = get_last_hour_date_info()
    mcdb.cursor.execute("SELECT time, latency FROM mcstatus WHERE time >= ?", (one_hour_ago, ))
    rows = mcdb.cursor.fetchall()
    
    data = [{"time": parse_date_to_h_m_s(row[0]), "latency": row[1]} for row in rows]
    return data


@app.post("/restart-server")
async def restart_mc_server(password: Password):
    if PASSWORD != password.code:
        return {
            "status": "fail",
            "msg": "密码错误"
        }
    
    try:
        async with aiohttp.ClientSession() as asession:
            async with asession.post(RCON_SERVER, 
                                    json={"code": password.code}) as resp1:
                result1 = await resp1.json()

        return {
            "status": "成功",
            "msg": "重启指令已发送，请耐心等待1分钟，或者查看图表观察服务器是否正常上线"
        }
    except Exception:
        return {
            "status": "失败",
            "msg": "重启指令发送失败，请重试或者联系管理员"
        }



if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=10000)