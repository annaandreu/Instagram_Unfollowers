from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 

#username = input("Enter your username: ")
#password = input("Enter your password: ")

username = "github_test"
password = "hello_world!"

#global variable to keep track of number of followers/following
count = 0 

#input user and pass and then login
def login(driver):
    driver.find_element(By.NAME,"username").send_keys(username)
    driver.find_element(By.NAME,"password").send_keys(password)
    driver.find_element(By.NAME,"password").send_keys(u'\ue007')

#find button with specific css selector and click it
def click_button_with_css(driver, css_selector):
    element = WebDriverWait(driver, 30).until(
          EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
    element.click()

def click_button_with_xpath(driver, xpath):
    element = WebDriverWait(driver, 30).until(
          EC.element_to_be_clickable((By.XPATH, xpath)))
    element.click()

#get into profile tab
def navigate_to_profile(driver):
    profile_css = '[alt*="' + username + '"]'
    click_button_with_css(driver, profile_css)

#get usernames from both followers and following
def get_usernames_from_dialog(driver):
    list_xpath = '//div[@role="dialog"]//ul//li'
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, list_xpath)))
    
    scroll_down(driver)
    list_elems = driver.find_elements(By.XPATH, list_xpath)
    time.sleep(10000)

    users = []
    for i in range(0, len(list_elems)):
        try:
            row_text = list_elems[i].text
            if "Follow" in row_text:
                username = row_text[:row_text.index("\n")]
                users += [username]
        except: 
            print("continue")
    return users    


#scroll down to load all followers/following
def scroll_down(driver):
    global count 
    iter = 1
    while 1:
        scroll_top_num = str(iter * 1000)
        iter += 1
        driver.execute_script("document.querySelector('div[role=dialog] ul').parentNode.scrollTop=" + scroll_top_num)
        time.sleep(1)
        try:
            WebDriverWait(driver, 1).until(check_difference_in_count)
        except:
            count = 0
            break

    return 

#check if we have loaded all followers/following
def check_difference_in_count(driver):
    global count
    new_count = len(driver.find_elements(By.XPATH, '//div[@role="dialog"]//ul//li'))
    if new_count != count:
        count = new_count
        return True
    else:
        return False

def __main__():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(10)
    #WebDriverWait(driver, 30).until(EC.url_contains('/accounts/login/'))
    login(driver)
    navigate_to_profile(driver)
    time.sleep(10)
    #WebDriverWait(driver, 30).until(EC.url_contains('/' + username + '/'))

    followers_css = '[href=/"/ + username + /followers/]'
    close_css = '[aria-label="Close"]'
    following_css = 'a[href="/' + username + '/following/"]'

    click_button_with_css(driver, followers_css)
    time.sleep(10)
    followers_list = get_usernames_from_dialog(driver)
    
    click_button_with_css(driver, close_css)
    time.sleep(10)

    click_button_with_css(driver, following_css)
    following_list = get_usernames_from_dialog(driver)

    print(followers_list, following_list)

    time.sleep(1000)

    return  


__main__()

 