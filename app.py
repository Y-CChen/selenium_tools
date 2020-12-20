import argparse
import logging

from rich.logging import RichHandler


def _main():
    try:
        parsed_args = _parse_args()
        logger = logging.getLogger()
        logger.setLevel(logging.getLevelName(parsed_args.logging_level.upper()))
        logger.addHandler(RichHandler(rich_tracebacks=True))
    except Exception as e:
        logging.exception(e)


def _parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("-ll", "--logging-level", type=str, default="info", help="logging level")
    parsed_args = parser.parse_args(args)
    return parsed_args


if __name__ == "__main__":
    _main()
