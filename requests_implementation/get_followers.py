import insta_login
import sys
import time
from getpass import getpass

userList = insta_login.get_user_list('Famous_Users.txt')
if userList is None:
    print "Problem opening file"

username = raw_input('Enter username/email: ')
password = getpass()
session = insta_login.login(username, password)
if session is None:
    print "Problem logging in, please try again.."
    sys.exit(1)
for i in xrange(10):
    for user in userList:
        time.sleep(1)
        insta_login.follow_user(session, user)

    time.sleep(40)

    for user in userList:
        time.sleep(1)
        insta_login.unfollow_user(session, user)
    time.sleep(5)
    
