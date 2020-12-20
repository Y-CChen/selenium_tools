import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from .line_notify import line_notify


def arrival_noticing(line_notify_access_token, web_driver, urls, force_notify):
    products = dict()
    web_driver_wait = WebDriverWait(web_driver, 60)
    for url in urls:
        web_driver.get(url)
        product_name = web_driver.title
        product_name = product_name.split("|") if product_name else list()
        product_name = product_name[0].strip() if product_name else ""
        buy_now_button = _wait_until_visibility_of_element_located(
            web_driver_wait, (By.XPATH, "//*[@id='buyNowButton']")
        )
        in_stock = (not bool(buy_now_button.get_attribute("disabled"))) if buy_now_button else False
        products[product_name] = in_stock
    need_notify = force_notify
    messages = list()
    for product_name, in_stock in products.items():
        need_notify = need_notify or in_stock
        messages.append(
            "{:>16}: {}".format(
                {
                    True: "🟢 in stock",
                    False: "🔴 out of stock",
                }[in_stock],
                product_name,
            )
        )
    logging.info(messages)
    if need_notify:
        line_notify("\n".join(messages), line_notify_access_token)


def _wait_until_visibility_of_element_located(web_driver_wait, locator):
    return web_driver_wait.until(expected_conditions.visibility_of_element_located(locator))
