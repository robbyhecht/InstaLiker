# https://medium.com/better-programming/lets-create-an-instagram-bot-to-show-you-the-power-of-selenium-349d7a6744f7

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains

class InstaFollower():

    '''Constructor'''
    def __init__(self, username, password):
        self.driver = webdriver.Chrome("/Users/robbyhecht/chromedriver")
        self.username = username
        self.password = password
        self.driver.implicitly_wait(10)

    '''Sign into site'''
    def signIn(self): # self is the equivalent of driver as initialized above
        self.driver.get('https://www.instagram.com/accounts/login/')

        # capture username and password input fields
        userInput = self.driver.find_element_by_name('username')
        passwordInput = self.driver.find_element_by_name('password')

        # fields will be filled by designated credentials
        userInput.send_keys(self.username)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER) # then hit enter to submit form
        time.sleep(2) # wait for login

        # click "not now" for saving login info
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()

        # click "not now" for turning on notifications
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()

    '''Follow a single user'''
    def followWithUsername(self, username):
        self.driver.get('https://www.instagram.com/' + username + '/')
        time.sleep(2)
        followButton = self.driver.find_element_by_css_selector('button')
        if (followButton.text != 'Following'):
            followButton.click()
            time.sleep(2)
        else:
            print("You are already following this user")

    '''Unfollow the user'''
    def unfollowWithUsername(self, username):
        self.driver.get('https://www.instagram.com/' + username + '/')
        time.sleep(2)
        followButton = self.driver.find_elements_by_css_selector('button')[1]
        if (followButton.text != 'Follow'):
            followButton.click()
            time.sleep(2)
            confirmButton = self.driver.find_element_by_xpath('//button[text() = "Unfollow"]')
            confirmButton.click()
        else:
            print("You are not following this user")

    '''Print a list of user's followers'''
    def printUserFollowers(self, username, max):
        # go to user's page
        self.driver.get('https://www.instagram.com/' + username)
        # click the followers button to bring up followers modal
        followersLink = self.driver.find_element_by_css_selector('ul li a')
        followersLink.click()
        time.sleep(2) # wait for modal to load
        # capture the modal
        followersList = self.driver.find_element_by_css_selector('div[role=\'dialog\'] ul')
        # find length of the list of followers in the modal
        numFollowersInList = len(followersList.find_elements_by_css_selector('li'))
        followersList.click() # click on modal to enter

        # use action chain to move down the list until reaching designated max number
        actions = ActionChains(self.driver)
        actions.key_down(Keys.SPACE).key_up(Keys.SPACE)
        while (numFollowersInList < max):
            actions.perform()
            time.sleep(1)
            # print(numFollowersInList)
            numFollowersInList = len(followersList.find_elements_by_css_selector('li'))
            followersList.click()
        
        # initialize empty followers list
        followers = []
        # loop through followers
        for user in followersList.find_elements_by_css_selector('li'):
            # collect username
            userLink = user.find_element_by_css_selector('a').get_attribute('href')
            # print username
            print(userLink)
            # add username to list
            followers.append(userLink)
            # only break loop when reach max users
            if (len(followers) == max):
                break
        # return the followers list
        print(len(followers))
        return followers

    '''Close the browser window'''
    def closeBrowser(self):
        self.driver.close()

    '''Exit the test run and browser''' 
    def __exit__(self, exc_type, exc_value, traceback):
        self.closeBrowser()