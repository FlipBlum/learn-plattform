from jobs.news_generator import run as run_news
from jobs.video_aggregator import run as run_video
from jobs.gmail_parser import run as run_gmail


def test_news_generator_runs():
    run_news()


def test_video_aggregator_runs():
    run_video()


def test_gmail_parser_runs():
    run_gmail()
