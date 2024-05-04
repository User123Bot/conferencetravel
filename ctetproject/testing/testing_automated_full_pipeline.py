import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def type_like_a_human(element, text, delay=0.1):
    for char in text:
        element.send_keys(char)
        time.sleep(delay)


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


        # Wait for the city input to be visible
        city_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".city-input"))
        )



        type_like_a_human(city_input, "Canberra", delay=0.1)
        time.sleep(1)  # Wait for suggestions to appear
        suggestion = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".autocomplete-suggestions-one li"))
            )
        suggestion.click()  # Click the visible suggestion
        city_input.clear()

        time.sleep(1)



        
        type_like_a_human(city_input, "Tokyo", delay=0.1)
        time.sleep(1)  # Wait for suggestions to appear
        suggestion = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".autocomplete-suggestions-one li"))
            )
        suggestion.click()  # Click the visible suggestion
        city_input.clear()

        time.sleep(1)

  


        # Use JavaScript to click the right-arrow button directly
        driver.execute_script("document.querySelector('.right-arrow').click();")

        time.sleep(1)

        # Wait until the input fields are visible and interactable
        attendees_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".input-attendees"))
        )
        origin_city_input = driver.find_element(By.CSS_SELECTOR, ".input-origin")


        # Example data to enter
        type_like_a_human(attendees_input, "100", delay=0.1)  # Enter the number of attendees
        type_like_a_human(origin_city_input, "New York, United States", delay=0.1)

        time.sleep(1)

        # Click the 'Add' button to submit the data
        add_button = driver.find_element(By.CSS_SELECTOR, ".addButton")
        add_button.click()

        time.sleep(1)

        attendees_input.clear()  # Enter the number of attendees
        origin_city_input.clear()  # Enter the origin city

        # Update this to use the actual attribute of your input element
        file_input_locator = "browse-csv-button"
        file_input_element = driver.find_element(By.ID, file_input_locator)

        # Construct the absolute path to your CSV file
        current_dir = os.path.dirname(os.path.realpath(__file__))
        csv_file_path = os.path.join(current_dir, "testingcsv", "full_test_short.csv")

        # Use the send_keys method to input the path to your file
        file_input_element.send_keys(csv_file_path)

        time.sleep(1)

        # Wait for the results container to be visible
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".results-container"))
        )

        # Find all the result items
        results = driver.find_elements(By.CSS_SELECTOR, ".data-row")

        # Scroll through each result item
        for result in results:
            # Scroll the element into view using smooth behavior
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", result)
            time.sleep(1)  # Pause to allow for observation of the scroll action


        # Example data to enter
        type_like_a_human(attendees_input, "50", delay=0.1)  # Enter the number of attendees
        type_like_a_human(origin_city_input, "Canberra, Australia", delay=0.1)
        time.sleep(1)
        add_button.click()

        attendees_input.clear()  # Enter the number of attendees
        origin_city_input.clear()  # Enter the origin city

        time.sleep(1)

        # Example data to enter
        type_like_a_human(attendees_input, "20", delay=0.1)  # Enter the number of attendees
        type_like_a_human(origin_city_input, "Darwin, Australia", delay=0.1)
        time.sleep(1)
        add_button.click()

        attendees_input.clear()  # Enter the number of attendees
        origin_city_input.clear()  # Enter the origin city

        time.sleep(3)

        # Wait for the calculate button to be clickable
        calculate_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "Upload-CSV-button"))
        )

        # Click the calculate button
        calculate_button.click()
        driver.execute_script("document.getElementById('results').scrollIntoView({ behavior: 'smooth' });")

        time.sleep(20)


        # Add any assertions or additional steps here

    finally:
        driver.quit()


if __name__ == "__main__":
    test_csv_upload()
