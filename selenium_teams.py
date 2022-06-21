# from microsoft (e.g. graph.microsoft.com )
# https://github.com/ritvikkhanna09/AutoLoginBot/blob/master/script.py

import keyboard
import selenium
#from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from selenium.webdriver.common.keys import Keys
###########################################################

#enter the link to the website you want to automate login.


#enter your login username

#enter your login password
#to be safe, you'll have to enter your password manually
#password="corp_guest_wifi_password"

# http://10.255.255.254/logout.html

###########################################################

#enter the element for username input field
element_for_username="loginfmt"
#enter the element for password input field
element_for_password="passwd"
#enter the element for submit button
element_for_submit="idSIButton9"
#enter the element indicating the site works without a captive portal
teams_works="Microsoft Teams"
#teams_works="div.teams-title"

###########################################################


def main(outfile="teams.txt", url="https://teams.microsoft.com", username="dietzn@shure.com"):
         

    existing_browser = True
    session_url = "http://127.0.0.1:47015"
    session_id = "4d28c5c4f9aabfd96a9c5b11987363be"
    
    if not existing_browser:
        #browser = webdriver.Safari()    #for macOS users[for others use chrome vis chromedriver]
        browser = selenium.webdriver.Chrome('/snap/bin/chromium.chromedriver')    #uncomment this line,for chrome users
    
        # https://stackoverflow.com/questions/8344776/can-selenium-interact-with-an-existing-browser-session
        session_url = browser.command_executor._url       #"http://127.0.0.1:60622/hub"
        session_id = browser.session_id
        print(session_url)
        print(session_id)
        browser.get(url)
    else:
        browser = attach_to_session(session_url, session_id)

    # keyboard event handler
    def handle_keypress():
        log_current_chat(browser)
    
    #try:
    # check for a shure captive portal string to see if we need to sign in.
    # todo: try to handle captive portal (half baked idea... not related to teams scraping directly)
    
    time.sleep(1)

#    try:
#        # see if we need to sign in
#        captive = False
#        teams_element = browser.find_element_by_id(teams_works)
#    except selenium.common.exceptions.NoSuchElementException as e:
#        print('failed to find teams, try to log in')
##        captive = True
#        pass
    
    # sign in
#    if captive:
        # do this manually
        #try:
        #    username_element = browser.find_element_by_name(element_for_username)
        #    username_element.send_keys(username)        
        #    signInButton = browser.find_element_by_id(element_for_submit)
        #    signInButton.click()
        #    #password_element  = browser.find_element_by_name(element_for_password)
        #    #password_element.send_keys(password)
        #except selenium.common.exceptions.NoSuchElementException as e:
        #    captive = False
        #    # we're probably already logged in
        #    pass
#    else:
#        time.sleep(1)

    input("press key once logged in to teams and in correct chat")
    try:
        #teams_element = browser.find_element(By.XPATH, teams_works)
        if teams_works in browser.page_source:
            print('success')
        else:
            raise ValueError("ack")
    except selenium.common.exceptions.NoSuchElementException as e:
        print("giving up, can't reach teams")
        raise e
    
# more stale cruft for loggin in automatically... do manually

#    signInButton = browser.find_element_by_id(element_for_submit)
#    signInButton.click()
#    username_element = browser.find_element_by_name("username")
#    username_element.send_keys(username)
#    password_element = browser.find_element_by_name("password")
#    password_element.send_keys("blah")
#    #click sign in
#    e = browser.find_element_by_link_text("Call")
#    # wait for user to input code
#    #e.click()
#    #value = Verify
#    #Stay signed in?
#    e = browser.find_element_by_id(element_for_submit)
#    e.click()
#    #  id = idSIButton9
#    #signInButton.click() # manually
#    
#    #"Stay signed in?"
#    #click "Yes" id="idSIButton9"
#    
#    #todo: check that we're in teams

    # register global hotkey to start teams log
    # must be root on linux
    # todo: find another method
    #keyboard.add_hotkey('ctrl+shift+t', handle_keypress)
                        
    # # send ctrl-shift-2 to go to messages
    # # https://stackoverflow.com/questions/45902295/how-to-send-shortcut-keys-using-selenium-in-python-to-move-through-webpage
    # browser.find_element_by_tag_name('body').send_keys(Keys.CONTRL + Keys.SHIFT + '2')
    # # might need to press up a bunch of times to get to the top of the chat list
    # # select first chat
    # 
    # e = browser.switch_to.active_element
    # e.send_keys(Keys.ENTER)

    #keyboard.remove_all_hotkeys()
    log_current_chat(browser, outfile)
    #browser.quit()
    

    
def log_current_chat(browser, outfile):
    # start logging now
    # trigger this with a hotkey
    
    # select newest chat text
    e = browser.switch_to.active_element
    e.send_keys(Keys.SHIFT + Keys.TAB)
    # https://stackoverflow.com/questions/44834358/switch-to-an-iframe-through-selenium-and-python
    #browser.switch_to.frame(e)

    dump_complete = False
    prev_s = ""
    with open(outfile, 'a') as f:
        duplicate_count = 0
        while not dump_complete:
            # grab next element text
            e = browser.switch_to.active_element
            # grab string
            s = e.text
            #s = e.get_attribute('innerHTML')
            #s = e.get_attribute('innertext')
            print(e)
            print(s)
            e.send_keys(Keys.UP)
            try:
                browser.switch_to.frame(e)
            except:
                pass
            if s == prev_s:
                duplicate_count +=1
            else:
                duplicate_count = 0
            prev_s = s
            # if we see a lot of duplicates, we're probably at the top, so give up
            if duplicate_count > 10:
                dump_complete = True
            print(s, file=f)
    

# https://stackoverflow.com/questions/8344776/can-selenium-interact-with-an-existing-browser-session
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

# executor_url = driver.command_executor._url
# session_id = driver.session_id

def attach_to_session(executor_url, session_id):
    original_execute = WebDriver.execute
    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return original_execute(self, command, params)
    # Patch the function before creating the driver object
    WebDriver.execute = new_command_execute
    driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    driver.session_id = session_id
    # Replace the patched function with original function
    WebDriver.execute = original_execute
    return driver


# https://stackoverflow.com/questions/28889401/detect-user-key-mouse-in-python-selenium
#boppreh/keyboard
    
    
    #e = browser.switch_to.active_element; e.text
    #"11:36 PM\nI don't. Hold tight. It's not midnight yet. I said today. :-) Why are you up so late?"
    
    
    #e = browser.switch_to.active_element
    #e.text
    
    #arrow up to go back
    #e.text has message content
    #div id messageBody
    #name:
    #div class ts-msg-name app-small-font
    #timestamp:
    #div  div div div class timestamp-column span class ts-created message-datetime
    # save name, date, text, hash?
    # if name, date, text
    
    #if this hash is not in the hash table
    #    add this to the log and to the hash table
    #if it is in the hash table, we are done
    # unless there is a flag to go farther back (to scrape to the beginning of time, or some other limit)
    
    # determine if we are at the beginning of all messages (got same message over and over, pressing up?)
    
    
    #"repeat for next chat (unique group of users)"
    #"repeat for groups as well
    
    
    # then run ssl
    # ssl()
    
    
        #### to quit the browser uncomment the following lines ####
        # time.sleep(3)
        # browser.quit()
        # time.sleep(1)
        # browserExe = "Safari"
        # os.system("pkill "+browserExe)
    #except Exception:
        #### This exception occurs if the element are not found in the webpage.
    #    print("Some error occured :(")
    
        #### to quit the browser uncomment the following lines ####
        # browser.quit()
        # browserExe = "Safari"
        # os.system("pkill "+browserExe)

if __name__ == '__main__':
    main()

