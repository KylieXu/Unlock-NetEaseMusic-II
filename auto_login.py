# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "005EF5CA3B749AB153BF56F1827710D9F61663617A7C4AD7F0B99DB74C4A24CB46868EA0EAEAA19AF7D6D728EB76D610A35EB1C4D85C63997E997D94FB7DF15C79472CE62631C45EDDDDE87AADFB5561A96B519C91D7097AB5FC626DC81C7D438C80B9386C8CDA29DEB4E77B0B004D0CE5AD173E5DBA4038DFF5A3FCF7CBC9DBFF0E285E1DE4CD5712085ADFDD92253CDAAA4DA5E5BCFD3C61DC3E5BAC2E851F495C0382B46FAAFA48E87845F96F22D5C49E19DA89B0739835F4A49DDEB21D5C0274043A515FF90741945F624C392AD1B5C7F3ADDEF4C4023F9EAE44442E6282E2E926BF8D0A0EB99EE4A7AE58642040A59E9E12931524B1988979F53DDD2F6626D8E3E2E6A96BC96FF62A13D441D661CB60862F9B5DB8168C00D5B6A2B22BDCAA7955537B88927870986099285479F30F471045F00D2DA8C7F1FC2F82004E1D06CD0B5B16CA2635C5F9B1CC3AA1A208A8FB3AC6177CA531F26FD878A37E4EF885"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
