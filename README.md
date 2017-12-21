# cs_utilities.py


Function: **unshortenURL**(shortenedURL)

This function will take a shortened URL and follow the redirects until it gets the full URL and then returns that URL.  This function can unshorten urls that have been shortened multiple times and works with Twitter's shortener, Bit.ly, etc. It will return either the full URL if found or a None value if it fails to unshorten the URL.

*Usage Example:* 

import cs_utilities 

full_url = unshortenURL("https://t.co/ESfUXdcwyz")





# bulkTweet.py

Function: **statusesUpdate**(status,users,callback)

This function will bulk send tweets to a list of Twitter users via their screen name.  The first two parameters (status, users) are required.  The callback parameter allows passing a function that will be called after each attempt to tweet a user.  Two parameters are sent to the callback function (user,response).  The user is the screen_name of the Twitter user that a tweet was sent to and the response is the twitter response.  An example callback function is included to show how to handle the response.

*Usage Example*:


    def statusUpdateCallback(user, response):

        if 'errors' in response:
            print ("Tweet to user " + user + " failed.")

        if 'in_reply_to_screen_name' in response and response['in_reply_to_screen_name'] is not None:
            print ("Tweet to user " + user + " was successful.")

        if 'in_reply_to_screen_name' in response and response['in_reply_to_screen_name'] is None:
            print ("Tweet was successful but user mentioned is unknown or does not exist")
            
           
    friends = ["TwitterUser1","TwitterUser2","TwitterUser3"]
    statusesUpdate("Hello friends, hope you are doing well today!",friends)


