# login to instagram
import time
import requests
import random
import re
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

# Var init for session and login
header = {'Origin': 'https://www.instagram.com', 'Connection': 'keep-alive', 'Host': 'www.instagram.com', 'Accept-Language': 'en-US,en;q=0.8', 'Accept-Encoding': 'gzip, deflate', 'X-Instagram-AJAX': '1', 'Referer': 'https://www.instagram.com/', 'X-Requested-With': 'XMLHttpRequest', 'Content-Length': '0', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36'}
cookies = {'sessionid': '', 'mid': '', 'ig_pr': '1', 'ig_vw': '1920', 'csrftoken': '', 's_network': '', 'ds_user_id': ''}

BASE_URL = "https://www.instagram.com"

# Do the checkpoint with selenium then save the cookies to update the session.
# TODO change to use requests, or if not able then use ghost browser.
def checkpoint(url):
    cookies_dict={}
    browser = webdriver.Firefox()
    browser.get(url)
    assert "Instagram" in browser.title	# Make sure it loaded instagram correctly
    # Click send button
    sendButton = browser.find_element_by_xpath("//button[text()='Send Security Code']")
    sendButton.click()
    # Get code and enter it
    authCode = raw_input('Enter 6 digit code sent to your account email: ')
    codeInput = browser.find_element_by_name('security_code')
    codeInput.send_keys(authCode)
    codeInput.send_keys(Keys.RETURN)
    # Save cookies
    cookies_list = browser.get_cookies()
    for cookie in cookies_list:
        cookies_dict[cookie['name']] = cookie['value']
    # Quit
    browser.quit()
    return cookies_dict

# Get self id
def getUserId(page):
    return page.cookies.get_dict()['ds_user_id']


# Get user id for following him
def getFollowId(session, username):
    follow_page = session.get(BASE_URL + "/" + username + "/?__a=1")
    # Find first id - user id
    find_id = re.search('"id": "[0-9]+"', follow_page.text)
    # Extract id number from find_id
    follow_id = find_id.group(0)[7:-1]
    return follow_id


def login(user, password):
    # Init session
    session = requests.Session()
    session.cookies.update(cookies)
    session.headers.update(header)
    time.sleep(random.uniform(0.5, 3))
    # Set csrf token
    resp = session.get(BASE_URL)
    session.headers.update({'X-CSRFToken': resp.cookies['csrftoken']})
    time.sleep(random.uniform(0.5, 3))
    # Login
    login = session.post('https://www.instagram.com/accounts/login/ajax/', data={'password': password, 'username': user}, allow_redirects=True)
    token = login.cookies['csrftoken']
    session.headers.update({'X-CSRFToken': login.cookies['csrftoken']})
    # If connected succsessfuly
    if login.status_code == 200:
        print login.content
    # If needed checkpoint
    elif login.status_code == 400:
        # Go to checkpoint and set cookies as allowed cookies while keeping csrf token
        cookies_dict = checkpoint(BASE_URL + login.json()['checkpoint_url'])
        session.cookies.update(cookies_dict)
        session.cookies.update({'X-CSRFToken': token})
    else:
        print "problem connecting"
        return None
    return session

def follow_user(session, user_to_follow):
    if session is not None:
    	# Follow user
        followUser = session.post('https://www.instagram.com/web/friendships/' + getFollowId(session, user_to_follow) + '/follow/')
        print followUser.status_code
        print followUser.content

def unfollow_user(session, user_to_unfollow):
    if session is not None:
        # Unfollow user
        unFollowUser = session.post('https://www.instagram.com/web/friendships/' + getFollowId(session, user_to_unfollow) + '/unfollow/')
        print unFollowUser.status_code
        print unFollowUser.content

    
# How to follow someone:
# Be logged on to your account, with all the cookies in a session
# then use - session.post('https://www.instagram.com/web/friendships/{users-user-id}/follow')
# the post will hold ds_user_id that way he will know who followed who and will update accordingly
    
    
    
