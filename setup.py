# setup.py

import sys
from utilities.utils import print_warning, get_info_from_user, save_to_env, cleanup, setup_sender

if __name__ == '__main__':
    if '--sender' in sys.argv:
        setup_sender()
    elif '--user' in sys.argv:
        print_warning()
        user_info = get_info_from_user()
        save_to_env(user_info)
    elif '--clean' in sys.argv:
        cleanup()
    else:
        print("Invalid argument. Please use --sender, --user, or --clean.")
        sys.exit(1)