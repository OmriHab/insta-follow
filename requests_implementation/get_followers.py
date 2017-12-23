import insta_login
import sys
from getpass import getpass

username = raw_input('Enter username/email: ')
password = getpass()
session = insta_login.login(username, password)
if session is None:
    print "Problem logging in, please try again.."
    sys.exit(1)
insta_login.follow_user(session, 'matank001')
