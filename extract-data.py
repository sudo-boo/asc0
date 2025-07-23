from utilities.utils import *
from time import sleep
from utilities.ocr import perform_ocr
from datetime import datetime, timedelta
from selenium import webdriver
from utilities.email_engine import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://asc.iitb.ac.in/acadmenu/"
TRIM_PIXELS = [250, 20, 0, 0]
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 800

DELAY_MULTIPLIER = 1.2

ERRORS = []

def session_login(driver, user_info):
    # Switch to the rightPage frame
    try:
        frame = driver.find_element(By.NAME, "rightPage")
        driver.switch_to.frame(frame)
        sleep(0.5 * DELAY_MULTIPLIER)
        username_element = driver.find_element(By.NAME, "UserName")
        print_log("Username field found...", "info")
        username_element.send_keys(user_info.get_roll())
        print_log("Username entered...", "info")
        password_element = driver.find_element(By.NAME, "UserPassword")
        print_log("Password field found...", "info")
        password_element.send_keys(user_info.get_password())
        print_log("Password entered...", "info")
        sleep(0.5 * DELAY_MULTIPLIER)
        password_element.send_keys(Keys.RETURN)
        print_log(f"{green}Log in successfully...{reset}", "info")
        sleep(2 * DELAY_MULTIPLIER)
        return driver
    except Exception as e:
        print_log(f"{red}An error occurred while logging in: {e}{reset}", "error")
        return None

def iterate_years_and_semesters(driver):
    global DELAY_MULTIPLIER
    delay_multiplier = DELAY_MULTIPLIER
    
    # Switch to the correct frame if needed
    driver.switch_to.default_content()
    frame = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "rightPage"))
    )
    driver.switch_to.frame(frame)

    # Locate dropdowns & button
    year_dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "year")))
    semester_dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "semester")))
    submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "submit")))

    # Get all year options (except the last one)
    year_options = [option.get_attribute("value") for option in year_dropdown.find_elements(By.TAG_NAME, "option")][:-1]
    print_log(f"Year options: {year_options}", "info")

    # Get all semester options (except the last two)
    semester_options = [option.get_attribute("value") for option in semester_dropdown.find_elements(By.TAG_NAME, "option")][:-2]
    print_log(f"Semester options: {semester_options}", "info")

    # Sort options in descending order
    year_options.sort(reverse=True)
    semester_options.sort(reverse=True)

    for year in year_options:
        for semester in semester_options:
            try:
                # Re-fetch elements before interaction (avoids stale element errors)
                year_dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "year")))
                semester_dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "semester")))
                submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "submit")))

                # Select year & semester using JavaScript
                driver.execute_script("arguments[0].value = arguments[1];", year_dropdown, year)
                driver.execute_script("arguments[0].value = arguments[1];", semester_dropdown, semester)

                sleep(0.5 * delay_multiplier)  # Allow UI update

                # Click the submit button
                driver.execute_script("arguments[0].click();", submit_button)
                print_log(f"Selected Year {year}, Semester {semester}...", "info")

                # Wait for the page to load
                WebDriverWait(driver, 10).until(EC.staleness_of(submit_button))
                sleep(2 * delay_multiplier)

                # Now extract and iterate over department links
                iterate_department_links(driver)

            except Exception as e:
                print_log(f"Error while selecting Year {year}, Semester {semester}: {e}", "error")


def iterate_department_links(driver):
    try:
        # Wait for department links to be present
        department_links = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//tr/td/a[contains(@href, 'RunningCourses.jsp')]"))
        )

        # Extract relative hrefs and convert them to full URLs
        links = [URL + link.get_attribute("href") for link in department_links]

        for link in links:
            driver.get(link)  # Navigate to department page
            print_log(f"Visited department: {link}", "info")

            # Perform any department-specific actions here
            sleep(2 * DELAY_MULTIPLIER)  # Allow page load

            driver.back()  # Return to semester page
            sleep(1 * DELAY_MULTIPLIER)  # Allow page reload
            
    except Exception as e:
        print_log(f"Error while iterating department links: {e}", "error")

def session(session_number, delay_multiplier, user_info=None, time_stamp=None):
    global TIMESTAMPS, ERRORS
    
    print()
    print_log("=====================================================================================================")
    print_log(f"{yellow}Starting session number {session_number}...{reset}", "info")
    print_log("=====================================================================================================")
    print_log(f"{yellow}Loading Data....{reset}", "info")

    if user_info is None:
        print_log(f"{red}Error loading user information. Exiting...{reset}", "error")
        return

    print_log(f"{green}Data successfully loaded.!!{reset}", "info")
    print_log("=====================================================================================================")

    print_log(f"{yellow}Opening the browser and navigating to {URL}...{reset}")

    # Set up Chrome options for headless mode
    options = Options()
    # options.add_argument("--headless")  # Run in headless mode
    # options.add_argument("--disable-gpu")  # Disable GPU acceleration (needed for headless mode)
    # options.add_argument("--no-sandbox")  # Disable sandboxing (needed in certain environments)
    
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)
    print_log(f"Window size set to {WINDOW_WIDTH}x{WINDOW_HEIGHT}")

    try:
        driver.get(URL)

        # Wait for the frameset to be loaded
        sleep(1 * delay_multiplier)
        
        driver = session_login(driver, user_info)
        if driver is None:
            return

        # --------------After login -----------------

        # Switch to the leftPage frame
        driver.switch_to.default_content()
        frame = driver.find_element(By.NAME, "leftPage")
        driver.switch_to.frame(frame)
        
        # Expand the "Academic" node to reveal "All About Courses"
        academic_node = driver.find_element(By.XPATH, "//a[contains(text(), 'Academic')]")
        driver.execute_script("arguments[0].click();", academic_node)
        print_log("Clicked on 'Academic'...", "debug")
        sleep(0.5)

        # Expand the "All About Courses" node to reveal "Running Courses"
        all_about_courses_node = driver.find_element(By.XPATH, "//a[contains(text(), 'All About Courses')]")
        driver.execute_script("arguments[0].click();", all_about_courses_node)
        print_log("Clicked on 'All About Courses'...", "debug")
        sleep(0.5)

        running_courses_node = driver.find_element(By.XPATH, "//a[contains(text(), 'Running Courses')]")
        driver.execute_script("arguments[0].click();", running_courses_node)
        print_log("Clicking on 'Registration/Adjustment'...", "debug")

        sleep(0.5 * delay_multiplier)

        driver.switch_to.default_content()
        frame = driver.find_element(By.NAME, "rightPage")
        driver.switch_to.frame(frame)
        
        sleep(4 * delay_multiplier)
        
        # Iterate over all years and semesters
        iterate_years_and_semesters(driver)
        

    except Exception as e:
        print_log(f"An error occurred: {e}", "error")
        time_stamp = time_stamp.strftime("%Y%m%d_%H_%M_%S")
        error_img_path = get_error_output_path_by_timestamp(time_stamp)
        driver.save_screenshot(error_img_path)
        ERRORS.append((error_img_path, e, time_stamp))
        driver.quit()

def setup():
    print_log("=====================================================================================================")
    print_log(f"{yellow}Starting setup...{reset}", "info")
    print_log("Getting user information from the .env file...")
    user_info = get_details_from_env_file()
    if user_info is None:
        return None
    print_log(f"User information loaded successfully.")
    
    print_log("Creating output directories...")
    create_output_dirs()
    print_log("Output directories created successfully.")
    print_log(f"{green}Setup complete....{reset}", "info")
    print_log("=====================================================================================================")
    print()
    return user_info


if __name__ == '__main__':
    user_info = setup()
    if user_info is not None:
        # scheduler()
        session(1, 1, user_info, datetime.now())
    else:
        print_log(f"{red}Setup failed. Exiting...{reset}", "error")
        exit(1)

