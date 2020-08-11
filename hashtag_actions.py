from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By

class InstaLiker():

    def __init__(self, username, password):
        '''Constructor'''
        self.driver = webdriver.Chrome("/Users/robbyhecht/chromedriver")
        self.username = username
        self.password = password
        self.driver.implicitly_wait(10)

    def signIn(self):
        '''Sign into Website'''
        self.driver.get('https://www.instagram.com/accounts/login/')

        # capture username and password input fields
        userInput = self.driver.find_element_by_name('username')
        passwordInput = self.driver.find_element_by_name('password')
        # fields filled by designated credentials, then submit
        userInput.send_keys(self.username)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)
         # wait for login
        time.sleep(2)
        # click "not now" for saving login info
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
        # click "not now" for turning on notifications
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()

    def goToTag(self, tag):
        '''Navigate to a specified hashtag page'''
        # capture search field and enter hashtag
        searchField = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
        searchField.send_keys(tag)
        # select first dropdown option
        self.driver.find_elements_by_css_selector('.fuqBx a')[0].click()

    def LikeRecentPosts(self, amountOfLikes):
        '''Like recent tag posts without leaving a comment'''
        # go to the most recent (they are in a separate div from top posts)
        firstPost = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div/div[1]/div[1]')
        # click on first post
        firstPost.click()
        time.sleep(1)
        # access the new modal
        postModal = self.driver.find_element_by_css_selector('div[role=\'dialog\']')
        postModal.click()

        # like each post until complete:
        for i in range(amountOfLikes):
            # click the heart icon to like the post
            self.driver.find_element(By.CSS_SELECTOR, (".fr66n button")).click()
            # click right arrow to go to next post
            self.driver.find_element_by_class_name("coreSpriteRightPaginationArrow").click()

    def LikeAndCommentOnRecentPosts(self, amountOfLikesAndComments):
        '''Like recent tag posts and leave a "hands clapping emoji" comment'''
        # go to the most recent (they are in a separate div from top posts)
        firstPost = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div/div[1]/div[1]')
        # click on first post
        firstPost.click()
        time.sleep(1)
        # access the new modal
        postModal = self.driver.find_element_by_css_selector('div[role=\'dialog\']')
        postModal.click()

        # like and comment each post until complete:
        for i in range(amountOfLikesAndComments):
            # click the heart icon to like the post
            self.driver.find_element(By.CSS_SELECTOR, (".fr66n button")).click()
            # if comments are enabled...
            if self.driver.find_element_by_tag_name('textarea').is_displayed():
                # enter comment
                self.driver.find_element_by_tag_name('textarea').click()
                # bypass chromedriver blocking emojis and add hands clapping comment
                JS_ADD_TEXT_TO_INPUT = """
                var elm = arguments[0], txt = arguments[1];
                elm.value += txt;
                elm.dispatchEvent(new Event('change'));
                """
                textArea = self.driver.find_element_by_tag_name('textarea')
                text = "👏"
                self.driver.execute_script(JS_ADD_TEXT_TO_INPUT, textArea, text)
                # add a space to the comment to activate post button
                textArea.send_keys(" ")
                # click post button
                self.driver.find_elements(By.CSS_SELECTOR, ("form button"))[0].click()
            # click right arrow to go to next post
            self.driver.find_element_by_class_name("coreSpriteRightPaginationArrow").click()


    def closeBrowser(self):
        '''Close the browser window'''
        self.driver.close()

    def __exit__(self, exc_type, exc_value, traceback):
        '''Exit the test run and browser''' 
        self.closeBrowser()