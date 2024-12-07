# utils.py

import os
import shutil
from PIL import Image
from utilities.user_info import UserInfo

red = '\033[91m'
green = '\033[92m'
yellow = '\033[93m'
reset = '\033[0m'

def get_image_path_by_timestamp(timestamp):
    return f"outputs/ss/reg_page_{timestamp}.png"

def get_ocr_output_path_by_timestamp(timestamp):
    return f"outputs/ocr/reg_page_{timestamp}_ocr.txt"

def get_error_output_path_by_timestamp(timestamp):
    return f"outputs/error/reg_page_{timestamp}_error.png"

def print_log(message, level="info"):
    from datetime import datetime as dt
    """
    Print a log message to the console with the current timestamp.
    
    Args:
    message (str): The message to be printed.
    level (str): The log level (info, debug, error, warning).
    """
    print(f"[{dt.now().strftime('%Y-%m-%d %H:%M:%S')}] :: {level.upper()}\t:: {message}")

def trim_image(image_path, trim_pixels=[0, 0, 0, 0]):
    # Open the image using Pillow
    image = Image.open(image_path)
    width, height = image.size
    crop_box = (trim_pixels[0], trim_pixels[1], width - trim_pixels[2], height - trim_pixels[3])
    # Crop the image and save it
    cropped_image = image.crop(crop_box)
    cropped_image.save(image_path)  # Save the cropped image
    print_log(f"Image trimmed and saved as {image_path}")

# create ss directory if not exists
def create_output_dirs():
    if not os.path.exists('outputs'):
        os.makedirs('outputs')
    if not os.path.exists('outputs/ss'):
        os.makedirs('outputs/ss')
    if not os.path.exists('outputs/ocr'):
        os.makedirs('outputs/ocr')
    if not os.path.exists('outputs/error'):
        os.makedirs('outputs/error')

def get_details_from_env_file():
    """
    Reads the .env file to get USERNAME and PASSWORD.
    Returns a tuple (USERNAME, PASSWORD) if successful, or (None, None) if the file is not found.
    """
    if not os.path.exists('.env'):
        print_log("The file .env is not present in the current directory. Run the setup.py file to create the file.", "error")
        return None, None
    
    try:
        with open('.env', 'r') as f:
            lines = f.readlines()
            USERNAME = lines[0].split('=')[1].strip()
            PASSWORD = lines[1].split('=')[1].strip()
            EMAIL = lines[2].split('=')[1].strip()
            PHONE = lines[3].split('=')[1].strip()

            return UserInfo(USERNAME, PASSWORD, PHONE, EMAIL)
    except Exception as e:
        print_log(f"{red}Error reading .env file: {e}", "error")
        print_log(f"Please check the contents of the .env file created using setup.py and try again.{reset}", "error")
        return None, None
        
# Function to display a warning message about the collection of user data
def print_warning():
    print("=====================================================================================================")
    print_log(f"{yellow}This requires some information from the user, that will be further used for ASC Login...{reset}", "warn")
    print_log(f"{yellow}DO NOT WORRY! This info will only be stored in your local environment.{reset}", "warn")
    print_log(f"{yellow}Please make sure you enter the correct information.{reset}", "warn")
    print(f"=====================================================================================================")

# Function to prompt the user for their details (roll number, password, phone, and email)
def get_info_from_user():
    def check_email(email):
        if '@' in email and '.' in email:
            return True
        return False
        
    roll = input("Enter your Roll Number: ")
    password = input("Enter your Password: ")
    email = input("Enter your Email Address: ")
    while not check_email(email):
        print("Please enter a valid email address.")
        email = input("Enter your Email Address: ")
    phone = input("Enter your Phone Number: ")

    # Return a UserInfo object initialized with the user data
    return UserInfo(roll, password, phone, email)

# Function to save the user details into a .env file
def save_to_env(user_info):
    with open('.env', 'w') as f:
        f.write(f"ROLL={user_info.get_roll()}\n")
        f.write(f"PASSWORD={user_info.get_password()}\n")
        f.write(f"EMAIL={user_info.get_email()}\n")
        f.write(f"PHONE={user_info.get_phone()}\n")
        print(f"{green}=====================================================================================================")
        print(f"Information saved successfully!")
        print(f"====================================================================================================={reset}")

# delete .env file and outputs directory
def cleanup():
    # Remove .env file if it exists
    if os.path.exists('.env'):
        os.remove('.env')
        print_log(f".env file has been deleted successfully.")

    if os.path.exists('outputs'):
        shutil.rmtree('outputs')
        print_log("'outputs' directory and its contents have been deleted successfully.")

    # Also clean __pycache__ directories in all subdirectories
    for root, dirs, files in os.walk('.', topdown=True):
        if '__pycache__' in dirs:
            pycache_dir = os.path.join(root, '__pycache__')
            shutil.rmtree(pycache_dir)
            print_log(f"'{pycache_dir}' directory and its contents have been deleted successfully.")

    print_log(f"{green}Cleanup completed successfully...{reset}")
    print_log("=====================================================================================================")