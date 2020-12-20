import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


def arrival_noticing(web_driver, urls):
    products = dict()
    web_driver_wait = WebDriverWait(web_driver, 60)
    for url in urls:
        web_driver.get(url)
        product_name = _wait_until_visibility_of_element_located(
            web_driver_wait, (By.XPATH, "/html/body/main/div[6]/div[3]/div[3]/h1")
        )
        product_name = product_name.text if product_name else ""
        buy_now_button = _wait_until_visibility_of_element_located(
            web_driver_wait, (By.XPATH, "//*[@id='buyNowButton']")
        )
        in_stock = (not bool(buy_now_button.get_attribute("disabled"))) if buy_now_button else False
        products[product_name] = in_stock
    logging.debug(products)


def _wait_until_visibility_of_element_located(web_driver_wait, locator):
    return web_driver_wait.until(expected_conditions.visibility_of_element_located(locator))
