import tweepy
import random
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

CONSUMER_KEY = 'vBFf6NvpwP7tzpSgYRVpfHMf4'
CONSUMER_SECRET = 'XEUkglke1h6siqigEOpGeFjnA9BaR4HjHGngT6WtJl0ENfkJKL'
ACCESS_KEY = '1282749495688781825-2YxepjxeVTMuNYlZMy3PHsbV4d3J3E'
ACCESS_SECRET = 'H9D2yw3EtwvuDTY3bkWA5287CN1w0jdrBRbPoZvJni8Em'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

LAST_SEEN = "last_seen_id.txt"

twitterHandle = "bookbot0"

def retrieve_last_seen_id(LAST_SEEN):
    f_read = open(LAST_SEEN, 'r')
    last_seen_id = (f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, LAST_SEEN):
    f_write = open(LAST_SEEN, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return 

def search_book(bookRequest):
    print("Searching for book..")
    driver = webdriver.Chrome()
    driver.get("http://libgen.is/")
    elem = driver.find_element_by_name("req")
    elem.clear()
    elem.send_keys(bookRequest)
    elem.send_keys(Keys.ENTER)

    try: # Search for title in libgen.is
        link = driver.find_element_by_link_text("[3]")
        link.click()
    except NoSuchElementException:
        response = " Sorry your book was not found :/ did you spell it correctly?"
    try: # search for title in b-ok
        zLibLink = driver.find_element_by_partial_link_text(bookRequest)
        zLibLink.click()
        response = " Here you go! :) " + driver.current_url
    except NoSuchElementException:
        response = " Sorry your book was not found :/ did you spell it correctly?"

    return response

def reply_to_tweets():
    print("Looking for mentions...")
    last_seen_id = retrieve_last_seen_id(LAST_SEEN)
    mentions = api.mentions_timeline(last_seen_id)

    # look through all tweets
    for mention in reversed(mentions):
        print(str(mention.id) + " - " + mention.text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, LAST_SEEN)

        if "#bookbot" in mention.text.lower():
            # format tweet for searching
            bookRequest = mention.text
            bookRequest = bookRequest.replace(" #BookBot","")
            bookRequest = bookRequest.replace(twitterHandle + " ","")
            # get response
            response = search_book(bookRequest)
            # respond
            api.update_status("@" + mention.user.screen_name  + response, mention.id)
            print("Replied to: @" + mention.user.screen_name)



while True:
    reply_to_tweets()
    time.sleep(15)