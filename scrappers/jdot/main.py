from time import sleep

from exceptiongroup import catch
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from helpers import download_image_from_url
from settings import JDOT_DIR, JDOT_LOGO_DIR

# A primary url for the site
MAIN_SITE_URL = 'https://www.junaidjamshed.com/'

navigation_urls = []

# open the site
def open_website() -> WebDriver:
    driver = get_the_driver()
    driver.get(MAIN_SITE_URL)
    return driver

# select the country to pakistan
def select_the_country(driver: WebDriver) -> None:
    dropdown = Select(driver.find_element(By.ID, 'landing-currency'))
    dropdown.select_by_value('AUD')
    dropdown.select_by_value('PKR')
    button = driver.find_element(By.CSS_SELECTOR, 'button.jj-enter-btn')
    button.click()
    sleep(25)

# crawl the navigation and fetch all the navigation urls
def crawl_the_navigation(driver: WebDriver) -> None:
    navigation = driver.find_element(By.XPATH, '//*[@id="store.menu"]/nav')
    hyperlinks = navigation.find_elements(By.TAG_NAME, 'a')

    for hyperlink in hyperlinks:
        link = hyperlink.get_attribute('href')
        try:
            name_elem = hyperlink.find_element(By.CSS_SELECTOR, 'span.mm-subcategory-title.underline-megamenu')
            name = name_elem.text

            # If text is empty, try using JavaScript to extract the text content
            if not name:
                name = driver.execute_script("return arguments[0].textContent;", name_elem).strip()

            navigation_urls.append({
                'link': link,
                'name': name
            })
        except NoSuchElementException:
            continue

    print(navigation_urls)

# get the selenium driver
def get_the_driver() -> WebDriver:
    return webdriver.Chrome()

# init the whole setup
def init() -> None:
    driver = open_website()
    download_logo(driver)
    select_the_country(driver)
    crawl_the_navigation(driver)
    driver.close()

# download the logo of the site
def download_logo(driver: WebDriver) -> None:
    logo_img = driver.find_element(By.XPATH, '//*[@id="maincontent"]/div[2]/div/div[4]/div/img')
    img_src = logo_img.get_attribute('src')
    download_image_from_url(img_src, JDOT_DIR+'/'+JDOT_LOGO_DIR)
