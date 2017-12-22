from instaLike import instaLike
from getpass import getpass

def main():
    print "Enter instagram login"
    # Get username and password
    user = raw_input("Username: ")
    password = getpass()
    
    # Connect to instagram
    instaFollower = instaLike()
    instaFollower.logIn(user, password)
    user_to_follow = raw_input("Enter user to follow: ")
    if instaFollower.follow(user_to_follow) == 1:
        print user_to_follow + " followed!"
    else:
        print "Error following or already followed"
    # TODO return different value for error and already followed
    
if __name__ == '__main__':
    main()
