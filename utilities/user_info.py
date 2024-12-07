# user_info.py
class UserInfo:
    def __init__(self, roll, password, phone, email):
        """
        Initializes the UserInfo object with the provided details.
        
        :param roll: The roll number of the user
        :param password: The password of the user
        :param phone: The phone number of the user
        :param email: The email address of the user
        """
        self.roll = roll
        self.password = password
        self.phone = phone
        self.email = email

    def get_roll(self):
        """
        Returns the roll number of the user.
        
        :return: User's roll number
        """
        return self.roll

    def get_password(self):
        """
        Returns the password of the user.
        
        :return: User's password
        """
        return self.password

    def get_phone(self):
        """
        Returns the phone number of the user.
        
        :return: User's phone number
        """
        return self.phone

    def get_email(self):
        """
        Returns the email address of the user.
        
        :return: User's email address
        """
        return self.email
