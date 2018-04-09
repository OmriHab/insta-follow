from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

class instaLike:
    def __init__(self):
        self.instagramBrowser = webdriver.Firefox()
        self.instagramBrowser.get("https://www.instagram.com/accounts/login/?force_classic_login")
        assert "Instagram" in self.instagramBrowser.title	# Make sure it loaded instagram correctly
    
    def logIn(self, user, password):
        '''
         Log in to instagram, take care of all cases
        '''
        self.Error = 0
        self.Success = 1
        
    # Check if logged in already
        if self.isLoggedIn():
            return self.Success
        
    # Try to log in using username and password
        try:
            self.userElem = self.instagramBrowser.find_element_by_name("username")
            self.userElem.clear()
            self.userElem.send_keys(user)
            self.passElem = self.instagramBrowser.find_element_by_name("password")
            self.passElem.clear()
            self.passElem.send_keys(password)
            self.passElem.send_keys(Keys.RETURN)
        except NoSuchElementException:
            return self.Error
        
    # Check if log in succesful
        if self.isLoggedIn():
           return self.Success
        else:
            return self.Error
        
    def follow(self, user_to_follow):
        if not self.isLoggedIn():
            return self.Error
        # Go to user page
        self.instagramBrowser.get("http://www.instagram.com/" + user_to_follow)
        # Try to click on the follow button
        try:
            self.followElement = self.instagramBrowser.find_element_by_xpath("//button[text()='Follow']")
            self.followElement.click()
        except NoSuchElementException:
            return self.Error
    
    def isLoggedIn(self):
        try:
            self.htmlTab = self.instagramBrowser.find_element_by_tag_name("html")
            if " logged-in" in htmlTab.get_attribute("class"):
                return True
            else:
                return False
        except:
            return False
    
