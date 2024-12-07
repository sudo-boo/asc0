from utils import *
from time import sleep
from utilities.ocr import perform_ocr
from datetime import datetime, timedelta
from selenium import webdriver
from utilities.email_engine import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

URL = "https://asc.iitb.ac.in/acadmenu/"
TRIM_PIXELS = [250, 20, 0, 0]
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 800
DELAY_MULTIPLIER = 1.0
NUM_EXCEEDS = 0
TIMESTAMPS = []
EXECUTION_TIME_THRESHOLD_HARD = 90
EXECUTION_TIME_THRESHOLD_SOFT = 30
EXECUTION_TIMES = []

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
        sleep(2 * DELAY_MULTIPLIER)
        print_log(f"{green}Logged in successfully...{reset}", "info")
        return driver
    except Exception as e:
        print_log(f"{red}An error occurred while logging in: {e}{reset}", "error")
        return None
    
def plot_execution_times():
    global EXECUTION_TIMES
    import matplotlib.pyplot as plt
    plt.plot(EXECUTION_TIMES, marker='o', color='b', linestyle='--', linewidth=1)
    plt.xlabel('Session Number')
    plt.ylabel('Execution Time (s)')
    plt.grid(True)
    plt.title('Execution Time vs Session Number')
    plt.savefig('execution_times.png')

def compare_ocr_outputs(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
        if len(lines1) != len(lines2):
            return False
        for i in range(len(lines1)):
            if lines1[i] != lines2[i]:
                return False
    return True

def session(session_number, delay_multiplier, user_info=None, time_stamp=None):
    global TIMESTAMPS
    
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

    driver = webdriver.Chrome()
    driver.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)
    print_log(f"Window size set to {WINDOW_WIDTH}x{WINDOW_HEIGHT}")

    try:
        driver.get(URL)

        # Wait for the frameset to be loaded
        sleep(2 * delay_multiplier)
        
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

        registrations_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Registration')]")
        driver.execute_script("arguments[0].click();", registrations_link)
        print_log("Clicked on 'Registrations'...", "debug")
        sleep(0.5)

        sub_reg_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Registration/Adjustment')]")
        driver.execute_script("arguments[0].click();", sub_reg_link)
        print_log("Clicking on 'Registration/Adjustment'...", "debug")

        sleep(1.5 * delay_multiplier)

        driver.switch_to.default_content()
        frame = driver.find_element(By.NAME, "rightPage")
        driver.switch_to.frame(frame)

        time_stamp = time_stamp.strftime("%Y%m%d_%H_%M_%S")
        # save in subdirectory
        screenshot_filename = get_image_path_by_timestamp(time_stamp)
        
        # Save the screenshot with the timestamped filename
        driver.save_screenshot(screenshot_filename)
        print_log(f"Screenshot saved in {screenshot_filename}")
        
        # Trim the top of the screenshot
        trim_image(screenshot_filename, TRIM_PIXELS)
        perform_ocr(screenshot_filename)

        # compare the ocr output with the latest ocr output
        if len(TIMESTAMPS) > 0:
            latest_timestamp = TIMESTAMPS[-1]
            latest_ocr_output = get_ocr_output_path_by_timestamp(latest_timestamp)
            current_ocr_output = get_ocr_output_path_by_timestamp(time_stamp)
            if not compare_ocr_outputs(latest_ocr_output, current_ocr_output):
                print_log(f"{red}DIFF SPOTTED: OCR outputs are different! Sending an email...{reset}", "warn")
                attachment_paths = [get_image_path_by_timestamp(latest_timestamp), get_image_path_by_timestamp(time_stamp)]
                send_email_with_attachment(time_stamp, attachment_paths)
            else:
                print_log(f"{green}OCR outputs are the same!{reset}", "info")

        TIMESTAMPS.append(time_stamp)
        print_log(f"{green}Session {session_number} completed successfully!{reset}", "info")
        print_log("=====================================================================================================\n")

    except Exception as e:
        print_log(f"An error occurred: {e}", "error")
        timestamp = datetime.now().strftime("%Y%m%d_%H_%M_%S")
        driver.save_screenshot(f'error_screenshot_{timestamp}.png')
        
    finally:
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


def scheduler():
    global DELAY_MULTIPLIER, NUM_EXCEEDS, EXECUTION_TIMES
    print_log(f"{yellow}Current time is \t{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{reset}")
    
    now = datetime.now()
    next_run = now.replace(microsecond=0, second=(30 if now.second < 30 else 0), minute=now.minute + (1 if now.second >= 30 else 0))
    
    print_log(f"{yellow}Next run will be at \t{next_run.strftime('%Y-%m-%d %H:%M:%S')}{reset}")
    
    session_number = 1
    while True:
        now = datetime.now()
        if now >= next_run:
            start = datetime.now()
            # session(session_number, DELAY_MULTIPLIER, user_info, next_run)
            sleep(10)
            if session_number == 1:
                sleep(2)
            if session_number == 2:
                sleep(5)
            if session_number == 3:
                sleep(1)
            end = datetime.now()
            execution_time = end - start
            if execution_time.total_seconds() > EXECUTION_TIME_THRESHOLD_HARD or NUM_EXCEEDS > 20:
                print_log(f"{red}Execution took too long: {execution_time} seconds{reset}", "error")
                send_TLE_email()
                break
            elif execution_time.total_seconds() > EXECUTION_TIME_THRESHOLD_SOFT:
                print_log(f"{red}Execution took longer than expected: {execution_time} seconds{reset}", "warn")
                DELAY_MULTIPLIER = (NUM_EXCEEDS + 1) ** 0.25
                NUM_EXCEEDS += 1
            else:
                print_log(f"Execution time was normal: {execution_time} seconds{reset}", "info")
                DELAY_MULTIPLIER = 1.0
                NUM_EXCEEDS = 0
            
            print_log(f"Session {session_number} completed in {end - start} seconds.")
            session_number += 1
            
            # Calculate the next valid run time based on the current time
            next_run = next_run + timedelta(seconds=30)
            now = datetime.now()
            if next_run <= now:
                next_run = now.replace(microsecond=0, second=(30 if now.second < 30 else 0), minute=now.minute + (1 if now.second >= 30 else 0))
            
            EXECUTION_TIMES.append(execution_time.total_seconds())
            plot_execution_times()
            
            print_log(f"{yellow}Current time is \t{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{reset}")
            print_log(f"{yellow}Next run will be at \t{next_run.strftime('%Y-%m-%d %H:%M:%S')}{reset}")
            print()
        else:
            sleep(1)  # Sleep for a short interval to avoid busy waiting


if __name__ == '__main__':
    user_info = setup()
    if user_info is not None:
        scheduler()
    else:
        print_log(f"{red}Setup failed. Exiting...{reset}", "error")
        exit(1)

