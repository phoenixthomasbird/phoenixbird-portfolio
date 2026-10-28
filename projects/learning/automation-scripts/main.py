#import the User class from class.py

from user import User
from datetime import date

#create new user
new_user = User("Jane", "jane@gmail.com", date.today())

print(new_user.info())