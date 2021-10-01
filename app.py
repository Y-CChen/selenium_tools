import argparse
import atexit
import logging
import time

from apscheduler.schedulers.background import BackgroundScheduler
from rich.logging import RichHandler

from config import Config
from selenium_tools import costco, make_web_driver


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
            scheduler.add_job(func=lambda: _job_costco_arrival_noticing(False), trigger="cron", minute="*/10")
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
            Config.LINE_NOTIFY_ACCESS_TOKEN, web_driver, Config.COSTCO_ARRIVAL_NOTICING_URLS, force_notify
        )


if __name__ == "__main__":
    _main()
