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

        # Update this to use the actual attribute of your input element
        file_input_locator = "browse-csv-button"
        file_input_element = driver.find_element(By.ID, file_input_locator)

        # Construct the absolute path to your CSV file
        current_dir = os.path.dirname(os.path.realpath(__file__))
        csv_file_path = os.path.join(current_dir, "testingcsv", "full_test_short.csv")

        # Use the send_keys method to input the path to your file
        file_input_element.send_keys(csv_file_path)

        time.sleep(3)

    finally:
        driver.quit()


if __name__ == "__main__":
    test_csv_upload()
