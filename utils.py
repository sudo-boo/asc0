# utils.py

from user_info import UserInfo
import os


red = '\033[91m'
green = '\033[92m'
yellow = '\033[93m'
reset = '\033[0m'
reset = '\033[0m'


def get_details_from_env_file():
    """
    Reads the .env file to get USERNAME and PASSWORD.
    Returns a tuple (USERNAME, PASSWORD) if successful, or (None, None) if the file is not found.
    """
    if not os.path.exists('.env'):
        print("The file .env is not present in the current directory. Run the setup.py file to create the file.")
        return None, None
    
    try:
        with open('.env', 'r') as f:
            lines = f.readlines()
            USERNAME = lines[0].split('=')[1].strip()
            PASSWORD = lines[1].split('=')[1].strip()
            return USERNAME, PASSWORD
    except Exception as e:
        print(f"Error reading .env file: {e}")
        return None, None

        
# Function to display a warning message about the collection of user data
def print_warning():
    print("=====================================================================================================")
    print(f"{yellow}WARNING:: This requires some information from the user, that will be further used for ASC Login...")
    print("DO NOT WORRY! This info will only be stored in your local environment.")
    print("Please make sure you enter the correct information.")
    print("=====================================================================================================")
    print(reset)

# Function to prompt the user for their details (roll number, password, phone, and email)
def get_info():

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
        f.write(f"PHONE={user_info.get_phone()}\n")
        f.write(f"EMAIL={user_info.get_email()}\n")
        print(f"{green}=====================================================================================================")
        print(f"Information saved successfully!")
        print(f"====================================================================================================={reset}")