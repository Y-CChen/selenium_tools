import logging
import random
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


def _random_sleep():
    time.sleep(random.randrange(5, 20) / 10)


def _seconds(text):
    return sum(x * int(t if t else 0) for x, t in zip([1, 60, 3600], text.split(":")[::-1]))


def _find_element(web_driver, web_driver_wait, by, value):
    web_driver_wait.until(expected_conditions.visibility_of_element_located((by, value)))
    _random_sleep()
    return web_driver.find_element(by, value)


def _search_and_play(web_driver, web_driver_wait, search_text, link_text, default_duration):
    logging.info(search_text)
    el = _find_element(
        web_driver, web_driver_wait, By.XPATH, '//input[@id="search" or @id="masthead-search-term"]'
    )
    el.click()
    el.clear()
    el.send_keys(search_text + Keys.RETURN)
    _random_sleep()
    ActionChains(web_driver).move_to_element(
        _find_element(web_driver, web_driver_wait, By.LINK_TEXT, link_text)
    ).click().perform()
    try:
        _find_element(
            web_driver, WebDriverWait(web_driver, 20), By.XPATH, '//div[@id="movie_player"]'
        )
    except TimeoutException:
        raise Exception("g-recaptcha")
    try:
        _find_element(
            web_driver,
            web_driver_wait,
            By.XPATH,
            '//button[starts-with(@class, "videoAdUiSkipButton") or starts-with(@class, "ytp-ad-skip-button")]',
        ).click()
    except TimeoutException:
        logging.error("ad skip button not found")
    _wait_streaming_finished(web_driver, web_driver_wait, default_duration)
    _random_sleep()


def _wait_streaming_finished(web_driver, web_driver_wait, default_duration):
    default_current = "00:00"
    duration = None
    current = None
    try:
        hover = (
            ActionChains(web_driver)
            .move_to_element(
                _find_element(web_driver, web_driver_wait, By.XPATH, '//div[@id="movie_player"]')
            )
            .move_by_offset(5, 5)
            .move_by_offset(-5, -5)
        )
        hover.perform()
        duration = _find_element(
            web_driver, web_driver_wait, By.XPATH, '//span[@class="ytp-time-duration"]'
        ).text
        hover.perform()
        current = _find_element(
            web_driver, web_driver_wait, By.XPATH, '//span[@class="ytp-time-current"]'
        ).text
    except TimeoutException:
        default_current = "01:00"
    finally:
        logging.info("{}/{}".format(current, duration))
        duration = duration if duration else default_duration
        current = current if current else default_current
        time.sleep(_seconds(duration) - _seconds(current))


def _clear_history(web_driver, web_driver_wait):
    try:
        _find_element(
            web_driver, web_driver_wait, By.XPATH, '//yt-icon-button[@id="guide-button"]'
        ).click()
        _find_element(web_driver, web_driver_wait, By.XPATH, '//a[@href="/feed/history"]').click()
        _find_element(
            web_driver,
            web_driver_wait,
            By.XPATH,
            "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div/ytd-browse-feed-actions-renderer/div/ytd-button-renderer[1]",
        ).click()
        _find_element(web_driver, web_driver_wait, By.XPATH, '//*[@id="confirm-button"]').click()
    except TimeoutException:
        logging.error("clear history failed")


def streaming(web_driver, streaming_list):
    products = dict()
    web_driver_wait = WebDriverWait(web_driver, 60)
    web_driver.get("https://www.youtube.com/")
    random.shuffle(streaming_list)
    logging.info("search and play")
    for streaming_item in streaming_list:
        _search_and_play(web_driver, web_driver_wait, *streaming_item)
    logging.info("clear history")
    _clear_history(web_driver, web_driver_wait)
    logging.info("delete cookies")
    web_driver.delete_all_cookies()
