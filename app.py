import argparse
import logging

from rich.logging import RichHandler

from config import Config
from selenium_tools import costco, make_web_driver


def _main():
    try:
        parsed_args = _parse_args()
        logger = logging.getLogger()
        logger.setLevel(logging.getLevelName(parsed_args.logging_level.upper()))
        logger.addHandler(RichHandler(rich_tracebacks=True))
        with make_web_driver(Config.WEB_DRIVER, Config.WEB_DRIVER_ARGS) as web_driver:
            if hasattr(Config, "COCST_ARRIVAL_NOTICING_URLS"):
                costco.arrival_noticing(web_driver, Config.COCST_ARRIVAL_NOTICING_URLS)
    except Exception as e:
        logging.exception(e)


def _parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("-ll", "--logging-level", type=str, default="info", help="logging level")
    parsed_args = parser.parse_args(args)
    return parsed_args


if __name__ == "__main__":
    _main()
