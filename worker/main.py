from apscheduler.schedulers.blocking import BlockingScheduler

from jobs.gmail_parser import run as run_gmail_parser
from jobs.news_generator import run as run_news_generator
from jobs.rss_fetcher import run as run_rss_fetcher
from jobs.video_aggregator import run as run_video_aggregator

scheduler = BlockingScheduler()

scheduler.add_job(run_gmail_parser, "interval", hours=1, id="gmail_parser")
scheduler.add_job(run_rss_fetcher, "interval", hours=2, id="rss_fetcher")
scheduler.add_job(run_news_generator, "interval", hours=6, id="news_generator")
scheduler.add_job(run_video_aggregator, "interval", hours=12, id="video_aggregator")

if __name__ == "__main__":
    print("Starting worker scheduler...")
    scheduler.start()
