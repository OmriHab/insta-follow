# login to instagram
import time
import requests
import random
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

cookies_dict={}

def checkpoint(url):
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

def getUserId(page):
    return page.cookies.get_dict()['ds_user_id']



def getFollowId(session, follow_url):
    follow_page = session.get(follow_url)
    tree = html.fromstring(homePage.text)
    follow_id_dict = tree.xpath('/html/body/script[@type="text/javascript"]')[0].text
    find_id = re.search('"id": "[0-9]+"', follow_id_dict)
    follow_id = find_id.group(0)[7:-1]

# Var init for session and login
header = {'Origin': 'https://www.instagram.com', 'Connection': 'keep-alive', 'Host': 'www.instagram.com', 'Accept-Language': 'en-US,en;q=0.8', 'Accept-Encoding': 'gzip, deflate', 'X-Instagram-AJAX': '1', 'Referer': 'https://www.instagram.com/', 'X-Requested-With': 'XMLHttpRequest', 'Content-Length': '0', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36'}
cookies = {'sessionid': '', 'mid': '', 'ig_pr': '1', 'ig_vw': '1920', 'csrftoken': '', 's_network': '', 'ds_user_id': ''}
user='omri.habibi@gmail.com'
password='******'


# Init session
session = requests.Session()
session.cookies.update(cookies)
session.headers.update(header)
time.sleep(random.uniform(0.5, 3))
# Set csrf token
resp = session.get('https://www.instagram.com/')
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
    checkpoint('https://www.instagram.com' + login.json()['checkpoint_url'])
    session.cookies.update(cookies_dict)
    session.cookies.update({'X-CSRFToken': token})
else:
    print "problem connecting"
    sys.exit(1)
# Follow user
userPage = session.get('https://www.instagram.com/matank001/')
followUser = session.post('https://www.instagram.com/web/friendships/' + getUserId(userPage) + '/follow')
print followUser.status_code
print followUser.content

    
# How to follow someone:
# Be logged on to your account, with all the cookies in a session, on your friends page
# then use - session.post('https://www.instagram.com/web/friendships/{YOUR-user-id}/follow')
    
    
    
