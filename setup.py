# setup.py

from utils import print_warning, get_info, save_to_env

# Main program execution
if __name__ == '__main__':
    print_warning()
    user_info = get_info()
    save_to_env(user_info)
    