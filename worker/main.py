from apscheduler.schedulers.blocking import BlockingScheduler

from jobs.gmail_parser import run as run_gmail_parser
from jobs.news_generator import run as run_news_generator
from jobs.video_aggregator import run as run_video_aggregator

scheduler = BlockingScheduler()

scheduler.add_job(run_news_generator, "interval", hours=6, id="news_generator")
scheduler.add_job(run_video_aggregator, "interval", hours=12, id="video_aggregator")
scheduler.add_job(run_gmail_parser, "interval", hours=1, id="gmail_parser")

if __name__ == "__main__":
    print("Starting worker scheduler...")
    scheduler.start()
