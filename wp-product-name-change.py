import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

driver = webdriver.Chrome()
driver.get('https://protecus.lt/wp-login.php?loggedout=true')
products_locator = "#menu-posts-product > a > div.wp-menu-name"
product_search_locator = "#post-search-input"

def find_element_with_retry(driver, locator):
    max_attempts = 3
    attempts = 0
    while attempts < max_attempts:
        try:
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, locator)))
            return element
        except StaleElementReferenceException as e:
            attempts += 1
            if attempts == max_attempts:
                raise e

    raise RuntimeError("Element is not found after maximum retries")

time.sleep(5)
find_element_with_retry(driver, products_locator).click()
driver.execute_script("window.scrollTo(50, 1080)")
search_input = find_element_with_retry(driver, product_search_locator)

search_input.click()
search_input.send_keys("pjovimo pjūklas")
search_input.send_keys(Keys.ENTER)

time.sleep(50)