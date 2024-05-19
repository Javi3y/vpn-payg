from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .tasks import print_something, update_session
scheduler = AsyncIOScheduler()

#scheduler.add_job(print_something, 'interval', seconds=3)
scheduler.add_job(update_session, 'interval', days=7)
