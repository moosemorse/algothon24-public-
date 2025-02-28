from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def submit_to_form(form_url, file_path):
    """
    Submit a file to a Google Form.
    :param form_url: The URL of the Google Form.
    :param file_path: Path to the file to be uploaded.
    :return: True if successful, False otherwise.
    """
    logger.info("Submitting results to Google Form...")
    
    try:
        # Initialize Selenium WebDriver
        driver = webdriver.Chrome()  # Ensure you have the ChromeDriver installed and in PATH
        driver.get(form_url)
        wait = WebDriverWait(driver, 10)

        # Find and fill the file upload input
        file_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="file"]')))
        file_input.send_keys(os.path.abspath(file_path))

        # Submit the form
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Submit")]')))
        submit_button.click()

        logger.info("Form submitted successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error in form submission: {e}")
        return False
    finally:
        driver.quit()

# Example usage
if __name__ == "__main__":
    form_url = 'https://docs.google.com/forms/d/e/1FAIpQLSeUYMkI5ce18RL2aF5C8I7mPxF7haH23VEVz7PQrvz0Do0NrQ/viewform'
    file_path = 'algothon24/optimized_portfolio_formatted.txt'  # Path to your .txt file

    # Debugging: Print file path
    logger.info(f"Checking file path: {os.path.abspath(file_path)}")
    
    # Ensure the file exists
    if os.path.exists(file_path):
        logger.info("File exists. Proceeding with form submission...")
        success = submit_to_form(form_url, file_path)
        print(f"Submission successful: {success}")
    else:
        logger.error("The file does not exist. Please check the file path.")

