from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .tasks import update_session, update_balance
from datetime import datetime

scheduler = AsyncIOScheduler()

scheduler.add_job(update_session, "interval", days=7,next_run_time=datetime.now())
scheduler.add_job(update_balance, "interval", minutes=1,next_run_time=datetime.now())
