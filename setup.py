#s etup.py

import sys
from utils import print_warning, get_info_from_user, save_to_env, cleanup

if __name__ == '__main__':
    if '--clean' in sys.argv:
        cleanup()
    else:
        print_warning()
        user_info = get_info_from_user()
        save_to_env(user_info)