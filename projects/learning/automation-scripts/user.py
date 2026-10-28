
class User:
    #Constructor method (initializer)
    def __init__(self, user_name, email_address, date_joined):
        self.user_name = user_name #instance variable
        self.email_address = email_address
        self.date_joined = date_joined

    #method
    def info(self):
        return f"{self.user_name}, {self.email_address}, joined {self.date_joined}"
    
    