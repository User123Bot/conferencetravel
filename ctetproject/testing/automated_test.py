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

        # driver.execute_script("window.scrollBy(0, 500);")  # Scroll down by 500 pixels

        time.sleep(1)

        # Wait for the right-arrow button to be clickable, then click it to navigate to the second slide
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".right-arrow"))
        ).click()

        time.sleep(2)

        # Update this to use the actual attribute of your input element
        file_input_locator = "browse-csv-button"
        file_input_element = driver.find_element(By.ID, file_input_locator)

        # Construct the absolute path to your CSV file
        current_dir = os.path.dirname(os.path.realpath(__file__))
        csv_file_path = os.path.join(current_dir, "testingcsv", "full_test_short.csv")

        # Use the send_keys method to input the path to your file
        file_input_element.send_keys(csv_file_path)

        time.sleep(4)

        # Find and click the upload button by its name, id, or any attribute
        # Update the locator as per your button's attribute
        upload_button_locator = "Upload-CSV-button"  # Example CSS Selector
        upload_button = driver.find_element(By.ID, upload_button_locator)
        upload_button.click()

        time.sleep(3)

        # Add any assertions or additional steps here

    finally:
        driver.quit()


if __name__ == "__main__":
    test_csv_upload()
