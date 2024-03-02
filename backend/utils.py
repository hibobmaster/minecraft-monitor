from mcstatus import JavaServer
from mcstatus.status_response import JavaStatusResponse
from datetime import datetime, timedelta
from dateutil import parser
from pytz import timezone

from db import MCDB

async def getJavaServerStatus(host: str) -> JavaStatusResponse:
    return await (await JavaServer.async_lookup(host)).async_status()

async def getJavaServerLatency(host: str) -> float:
    status = await getJavaServerStatus(host)
    return status.latency

async def schedule_job(host: str, mcdb: MCDB):
    current_time = datetime.now(timezone("Asia/Shanghai"))
    try:
        latency = await getJavaServerLatency(host)
    except Exception as e:
        # 服务器连接失败，可能宕机了，把延迟设为10s秒
        latency = 10000
        print(e)
    mcdb.insert_time_and_latency(current_time, latency)

def get_last_hour_date_info():
    return (datetime.now(timezone("Asia/Shanghai")) - timedelta(hours=1))

def get_current_day_time_utc8():
    return datetime.now(timezone("Asia/Shanghai")).strftime('%H:%M:%S')


def parse_date_to_h_m_s(timestamp_str) -> str:
    timestamp = parser.parse(timestamp_str)
    formatted_timestamp = timestamp.strftime("%H:%M:%S")
    return formatted_timestamp