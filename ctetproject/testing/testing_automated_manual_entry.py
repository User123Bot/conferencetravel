import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_csv_upload():
    # Setup ChromeDriver
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # Navigate to your web application's upload page
        driver.get("http://localhost:3000")

        time.sleep(1)

        driver.execute_script("document.getElementById('calculator').scrollIntoView({ behavior: 'smooth' });")

        time.sleep(2)

        # Use JavaScript to click the right-arrow button directly
        driver.execute_script("document.querySelector('.right-arrow').click();")

        time.sleep(2)

        # Wait until the input fields are visible and interactable
        attendees_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".input-attendees"))
        )
        origin_city_input = driver.find_element(By.CSS_SELECTOR, ".input-origin")

        # Example data to enter
        attendees_input.send_keys("100")  # Enter the number of attendees
        origin_city_input.send_keys("New York, United States")  # Enter the origin city

        # Click the 'Add' button to submit the data
        add_button = driver.find_element(By.CSS_SELECTOR, ".addButton")
        add_button.click()


        time.sleep(3)

    finally:
        driver.quit()


if __name__ == "__main__":
    test_csv_upload()
