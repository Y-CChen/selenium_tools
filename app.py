import argparse
import atexit
import logging
import random
import time

from apscheduler import events
from apscheduler.schedulers.background import BackgroundScheduler
from rich.logging import RichHandler

from config import Config
from selenium_tools import costco, line_notify, make_web_driver, youtube


def _main():
    scheduler = None

    try:
        parsed_args = _parse_args()
        logger = logging.getLogger()
        logger.setLevel(logging.getLevelName(parsed_args.logging_level.upper()))
        logger.addHandler(RichHandler(rich_tracebacks=True))

        # scheduler
        scheduler = BackgroundScheduler()
        costco_arrival_noticing_urls = getattr(
            Config, "COSTCO_ARRIVAL_NOTICING_URLS", None
        )
        if costco_arrival_noticing_urls is not None:
            _job_costco_arrival_noticing(
                costco_arrival_noticing_urls, force_notify=True
            )
            scheduler.add_job(
                func=lambda: _job_costco_arrival_noticing(
                    costco_arrival_noticing_urls, force_notify=False
                ),
                trigger="cron",
                minute="*/10",
            )
        youtube_streaming_list = getattr(Config, "YOUTUBE_STREAMING_LIST", None)
        if youtube_streaming_list is not None:
            job_id = "_job_youtube_streaming"
            streaming_count = 0
            streaming_count_notified = 0

            def _add_job_youtube_streaming_listener(event):
                nonlocal streaming_count
                if event.job_id == job_id:
                    if not event.exception:
                        streaming_count += 1
                    _add_job_youtube_streaming(
                        scheduler, job_id, youtube_streaming_list
                    )

            _add_job_youtube_streaming(scheduler, job_id, youtube_streaming_list)
            scheduler.add_listener(
                _add_job_youtube_streaming_listener,
                events.EVENT_JOB_EXECUTED | events.EVENT_JOB_ERROR,
            )

            def _job_line_notify_youtube_streaming_count():
                nonlocal streaming_count_notified
                line_notify.line_notify(
                    "youtube streaming {} times, {} times today".format(
                        streaming_count, streaming_count - streaming_count_notified
                    ),
                    Config.LINE_NOTIFY_ACCESS_TOKEN,
                )
                streaming_count_notified = streaming_count

            scheduler.add_job(
                func=_job_line_notify_youtube_streaming_count,
                trigger="cron",
                hour="1",
            )
        scheduler.start()
        atexit.register(scheduler.shutdown)

    except Exception as e:
        logging.exception(e)
        return

    while True:
        try:
            input()
        except KeyboardInterrupt:
            scheduler.pause()
            break
        except Exception as e:
            logging.exception(e)


def _parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-ll", "--logging-level", type=str, default="info", help="logging level"
    )
    parsed_args = parser.parse_args(args)
    return parsed_args


def _job_costco_arrival_noticing(costco_arrival_noticing_urls, force_notify=False):
    with make_web_driver(Config.WEB_DRIVER, Config.WEB_DRIVER_ARGS()) as web_driver:
        costco.arrival_noticing(
            Config.LINE_NOTIFY_ACCESS_TOKEN,
            web_driver,
            costco_arrival_noticing_urls,
            force_notify,
        )


def _job_youtube_streaming(youtube_streaming_list):
    with make_web_driver(Config.WEB_DRIVER, Config.WEB_DRIVER_ARGS()) as web_driver:
        youtube.streaming(web_driver, youtube_streaming_list)


def _add_job_youtube_streaming(scheduler, job_id, youtube_streaming_list):
    time.sleep(random.randrange(5, 20) / 10)
    scheduler.add_job(
        func=lambda: _job_youtube_streaming(youtube_streaming_list), id=job_id
    )


if __name__ == "__main__":
    _main()
