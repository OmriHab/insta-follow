from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

WAIT_PASS_PAGE = 2.5
WAIT_PASS_CLICK = 1.7
WAIT_CELEB_FOLLOW = 30
WAIT_NEXT_RUN = 120

RUN_TIME = 5

def set_up_browser():
	browser = webdriver.Firefox()
	browser.get("https://www.instagram.com/accounts/login/?force_classic_login")
	return browser

def login(browser, user, passw):
	#LOGIN INSTAGRAM
	username = browser.find_element_by_name("username")
	password = browser.find_element_by_name("password")
	
	username.send_keys(user)
	password.send_keys(passw)
	password.send_keys(Keys.RETURN)
	
	time.sleep(WAIT_PASS_PAGE)

	if "challenge" in browser.current_url:
		send_code = browser.find_element_by_xpath("//button[text()='Send Security Code']")
		send_code.click()
		key = raw_input("Enter 6 digit code sent to you by email: ")
		enter_code = browser.find_element_by_name("security_code")
		enter_code.send_keys(key)
		enter_code.send_keys(Keys.RETURN)
		time.sleep(8)
	

def move_to_profile_page(browser, profile_name):
	#SEARCHING USERNAME
	browser.get("https://www.instagram.com/" + profile_name + "/")
	time.sleep(WAIT_PASS_PAGE)

def click_follow(browser, un_follow = False):
	#FOLLOW
	if un_follow:
		follow_button = browser.find_element_by_xpath("//button[text()='Following']")
	else:
		follow_button = browser.find_element_by_xpath("//button[text()='Follow']")

	follow_button.click()
	time.sleep(WAIT_PASS_CLICK)
	
	
def get_user_list(file_path):
    try:
        user_file = open(file_path, 'r')
    except IOError:
        print 'Error opening file ' + file_path
        return None
    # Split all lines
    user_list = user_file.read().split('\n')
    # Remove all empty strings
    user_list = [user for user in user_list if user != '']
    return user_list
    

celebs = get_user_list("/home/omri/code/python/pyCode/instaLike/requests_implementation/Famous_Users.txt")

#first set up
browser = set_up_browser()
login(browser, "omri_habibi", "omri11")


for run in xrange(RUN_TIME):
	
	print str(run) + "\n\nFollowing..."
	# Follow all celebreties in celebs
	for cel in celebs:
		try:
			move_to_profile_page(browser, cel)
			click_follow(browser, un_follow = False)
		except:
			pass
	
	# Wait 80 seconds before unfollowing
	time.sleep(60)
	print "\nUnfollowing..."
	# Unfollow all celebreties in celebs
	for cel in celebs:
		try:
			move_to_profile_page(browser, cel)
			click_follow(browser, un_follow = True)
		except:
			pass

	time.sleep(60)


browser.close()
print ("END!!!")
