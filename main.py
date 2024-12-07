from utils import get_details_from_env_file
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from time import sleep

url = "https://asc.iitb.ac.in/acadmenu/"

def main():
    USERNAME, PASSWORD = get_details_from_env_file()
    if USERNAME is None or PASSWORD is None:
        return  # Exit the script if no credentials are found

    print(f"Username: {USERNAME}")
    print(f"Password: {'*' * len(PASSWORD)}")

    # Initialize the WebDriver (make sure ChromeDriver is in PATH or provide path to it)
    driver = webdriver.Chrome()

    try:
        driver.get(url)

        # Wait for the frameset to be loaded
        sleep(2)  # Wait for 2 seconds to ensure the frames are loaded
        frame = driver.find_element(By.NAME, "rightPage")  # Or use By.ID or other selectors
        driver.switch_to.frame(frame)

        sleep(1)
        username_element = driver.find_element(By.NAME, "UserName")
        print("Username field found.")
        username_element.send_keys(USERNAME)
        print("Username entered.")
        password_element = driver.find_element(By.NAME, "UserPassword")
        print("Password field found.")
        password_element.send_keys(PASSWORD)
        print("Password entered.")

        sleep(2)
        
        password_element.send_keys(Keys.RETURN)

        sleep(2)

        # ----------------- After login -----------------

        driver.switch_to.default_content()
        frame = driver.find_element(By.NAME, "leftPage")
        driver.switch_to.frame(frame)
        
        # Expand the "Academic" node to reveal "All About Courses"
        academic_node = driver.find_element(By.XPATH, "//a[contains(text(), 'Academic')]")
        driver.execute_script("arguments[0].click();", academic_node)
        sleep(1)

        registrations_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Registration')]")
        print("Clicking on 'Registrations'")
        driver.execute_script("arguments[0].click();", registrations_link)
        sleep(1)


        sub_reg_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Registration/Adjustment')]")
        print("Clicking on 'Registration/Adjustment'")
        driver.execute_script("arguments[0].click();", sub_reg_link)

        sleep(1)

        # capture the screenshot of the page

        # switch back to the default content and switch to the rightPage frame
        driver.switch_to.default_content()
        frame = driver.find_element(By.NAME, "rightPage")
        driver.switch_to.frame(frame)
        print("Switched to rightPage frame")

        driver.save_screenshot('registration_page.png')
        sleep(1)

        print("Getting the page source")
        # print(driver.page_source)

        # Optionally, wait for the page to load (you may need to adjust this depending on your needs)
        driver.implicitly_wait(5)  # Wait for 5 seconds

    except Exception as e:
        print(f"An error occurred: {e}")
        driver.save_screenshot('error_screenshot.png')  # Take a screenshot for debugging purposes
    
    finally:
        # Close the browser after the task
        driver.quit()

if __name__ == '__main__':
    main()
