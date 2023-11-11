import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

driver = webdriver.Chrome()
driver.get('https://protecus.lt/wp-login.php?loggedout=true')
products_locator = "#menu-posts-product > a > div.wp-menu-name"
bulk_editor_locator = "#menu-posts-product > ul > li:nth-child(9) > a"
bulk_search_locator = "#woobe_filter_form_tools_panel > div > div.col-lg-6 > input[type=text]"
item_locator = "#product_row_43020 > td:nth-child(4)"
load_more_button_locator = "#advanced-table_wrapper > div:nth-child(3) > div.dataTables_paginate.paging_simple_numbers > a.paginate_button.next"

def find_element_with_retry(driver, locator):
    max_attempts = 3
    attempts = 0
    while attempts < max_attempts:
        try:
            wait = WebDriverWait(driver, 30)
            element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, locator)))
            return element
        except StaleElementReferenceException as e:
            attempts += 1
            if attempts == max_attempts:
                raise e

    raise RuntimeError("Element is not found after maximum retries")

def change_item_name(driver, item_locator, load_more_button_locator):
    items = driver.find_elements(By.CSS_SELECTOR, item_locator)

    for item in items:
        if not item.is_displayed():
            driver.execute_script("arguments[0].scrollIntoView(true);", item)

        element = WebDriverWait(driver, 20).until(EC.visibility_of(item))
        element.click()

        product_title_text = element.text
        replaced_product_text = product_title_text.replace("pjovimo diskas", "Diskinis pjūklas festool")

        element.click()
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.BACKSPACE)
        element.send_keys(replaced_product_text)
        element.send_keys(Keys.ENTER)


    load_more_button = find_element_with_retry(driver, load_more_button_locator)
    load_more_button.click()
    time.sleep(2)


time.sleep(8)
find_element_with_retry(driver, products_locator).click()
find_element_with_retry(driver, bulk_editor_locator).click()
driver.execute_script("window.scrollTo(5, 1080)")

time.sleep(5)
search_input = find_element_with_retry(driver, bulk_search_locator)

search_input.click()
search_input.send_keys("pjovimo diskas")
search_input.send_keys(Keys.ENTER)

change_item_name(driver, item_locator, load_more_button_locator)
time.sleep(50)