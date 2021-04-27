from apscheduler.schedulers.background import BackgroundScheduler
from sharesUpdater import sharesUpdate

def start():
	scheduler = BackgroundScheduler()
	scheduler.add_job(sharesUpdate.getNewSharesList, 'cron', day_of_week='mon-fri', hour=18, minute=00)
	scheduler.start()