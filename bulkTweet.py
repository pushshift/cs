import requests
from requests_oauthlib import OAuth1Session, OAuth1
import time
import sys
import oauth2 as oauth
import json



def statusesUpdate(status,users,callback=None):

    # This method will send a message to one or more Twitter users. This method requires a text body (var status | type = str) and a list
    # of Twitter usernames (var users | type = list or str) and will then send out the text body to all Twitter users in the users list.
    # A single user can also be passed to this method as a string. You can also pass a function that will be invoked immediately after
    # each tweet is attempted.  The user screen_name and Twitter response will be passed as two parameters to the function. If the tweet was successful and sent
    # to an existing user, the "in_reply_to_screen_name" will have the user's screen_name as its value.  If a tweet was successful but
    # sent to a user that doesn not exist, "in_reply_to_screen_name" will have a value of null.

    # CONSTANTS
    DELAY_BETWEEN_USER_TWEETS = 1000     # Milliseconds
    API_ENDPOINT = 'https://api.twitter.com/1.1/statuses/update.json'
    RETRY_LIMIT = 8

    # Convert users to list if str is passed for one user
    if not isinstance(users, list): users = [users]

    # SANITY CHECKS
    # Test total length of tweet to make sure none will exceed 280 characters.  The total length of a sent tweet will be the length of the status
    # and the length of the user's screen name + 2 characters for the "@" character and a space.

    status_length = len(status) + 2
    for user in users:
        total_length = len(user) + status_length
        if (total_length) > 280:
            raise ValueError("Status length is greater than 280 characters for user '" + user + "' Tweet would be " + str(total_length) + " characters.")

    auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)

    for user in users:
        if user[:1] == "@": user = user[1:]   # Remove @ if they were appended to the user names
        message = "@" + user + " " + status
        retry_attempts = 0
        while True:
            r = requests.post(API_ENDPOINT, params={"status":message}, auth=auth)
            status_code = r.status_code
            if (str(status_code)[:1] == "5"):
                wait_time = 2**retry_attempts
                time.sleep(wait_time)
                continue
            if (status_code == 400):
                raise RuntimeError("Authentication failure.")
            if (str(status_code)[:1] == "2"):
                if callback:
                    response = json.loads(r.text)
                    callback(user, json.loads(r.text))
                break
            retry_attempts += 1
            if retry_attempts == RETRY_LIMIT: break
        time.sleep(DELAY_BETWEEN_USER_TWEETS / 1000)


def statusUpdateCallback(user, response):
    # This code could update the database after each Tweet is sent, etc.
    # Basic Examples

    if 'errors' in response:
        print ("Tweet to user " + user + " failed.")

    if 'in_reply_to_screen_name' in response and response['in_reply_to_screen_name'] is not None:
        print ("Tweet to user " + user + " was successful.")

    if 'in_reply_to_screen_name' in response and response['in_reply_to_screen_name'] is None:
        print ("Tweet was successful but user mentioned is unknown or does not exist")


statusesUpdate("Hello there!  This is a mass tweet example.",["pushshift","@jasonbaumgartne"], statusUpdateCallback)

