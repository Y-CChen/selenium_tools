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
    try:
        parsed_args = _parse_args()
        logger = logging.getLogger()
        logger.setLevel(logging.getLevelName(parsed_args.logging_level.upper()))
        logger.addHandler(RichHandler(rich_tracebacks=True))

        # scheduler
        scheduler = BackgroundScheduler()
        if hasattr(Config, "COSTCO_ARRIVAL_NOTICING_URLS"):
            _job_costco_arrival_noticing(True)
            scheduler.add_job(
                func=lambda: _job_costco_arrival_noticing(False), trigger="cron", minute="*/10"
            )
        if hasattr(Config, "YOUTUBE_STREAMING_LIST"):
            job_id = "_job_youtube_streaming"
            streaming_count = 0

            def _add_job_youtube_streaming_listener(event):
                nonlocal streaming_count
                if event.job_id == job_id:
                    if not event.exception:
                        streaming_count += 1
                    _add_job_youtube_streaming(scheduler, job_id)

            _add_job_youtube_streaming(scheduler, job_id)
            scheduler.add_listener(
                _add_job_youtube_streaming_listener,
                events.EVENT_JOB_EXECUTED | events.EVENT_JOB_ERROR,
            )
            scheduler.add_job(
                func=lambda: line_notify.line_notify(
                    "youtube streaming {} times".format(streaming_count),
                    Config.LINE_NOTIFY_ACCESS_TOKEN,
                ),
                trigger="cron",
                hour="1",
            )
        scheduler.start()
        atexit.register(lambda: scheduler.shutdown())

    except Exception as e:
        logging.exception(e)
        return

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break
        except Exception as e:
            logging.exception(e)


def _parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("-ll", "--logging-level", type=str, default="info", help="logging level")
    parsed_args = parser.parse_args(args)
    return parsed_args


def _job_costco_arrival_noticing(force_notify):
    with make_web_driver(Config.WEB_DRIVER, Config.WEB_DRIVER_ARGS) as web_driver:
        costco.arrival_noticing(
            Config.LINE_NOTIFY_ACCESS_TOKEN,
            web_driver,
            Config.COSTCO_ARRIVAL_NOTICING_URLS,
            force_notify,
        )


def _job_youtube_streaming():
    with make_web_driver(Config.WEB_DRIVER, Config.WEB_DRIVER_ARGS) as web_driver:
        youtube.streaming(web_driver, Config.YOUTUBE_STREAMING_LIST)


def _add_job_youtube_streaming(scheduler, job_id):
    time.sleep(random.randrange(5, 20) / 10)
    scheduler.add_job(func=_job_youtube_streaming, id=job_id)


if __name__ == "__main__":
    _main()
