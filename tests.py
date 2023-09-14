from apscheduler.schedulers.background import BackgroundScheduler

def my_job():
    print("Hello, World!")

scheduler = BackgroundScheduler()
scheduler.add_job(my_job, 'interval', seconds=1)
scheduler.start()

try:
    # Keeps the script running
    while True:
        pass
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
