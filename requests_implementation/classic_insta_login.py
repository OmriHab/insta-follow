import time
import requests
import random

header = {'Origin': 'https://www.instagram.com', 'Connection': 'keep-alive', 'Host': 'www.instagram.com', 'Accept-Language': 'en-US,en;q=0.8', 'Accept-Encoding': 'gzip, deflate', 'X-Instagram-AJAX': '1', 'Referer': 'https://www.instagram.com/', 'X-Requested-With': 'XMLHttpRequest', 'Content-Length': '0', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36'}
cookies = {'sessionid': '', 'mid': '', 'ig_pr': '1', 'ig_vw': '1920', 'csrftoken': '', 's_network': '', 'ds_user_id': ''}
user='omri.habibi@gmail.com'
password='omri11'

session = requests.Session()
session.cookies.update(cookies)
session.headers.update(header)
time.sleep(random.uniform(0.5, 3))
resp = session.get('https://www.instagram.com/')
token = resp.cookies['csrftoken']
session.headers.update({'X-CSRFToken': token})
time.sleep(random.uniform(0.5, 3))
login = session.post('https://www.instagram.com/accounts/login/?force_classic_login', data={'username': user, 'password': password, 'csrfmiddlewaretoken': token}, allow_redirects=True)

