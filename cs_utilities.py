import requests
import time

def unshortenURL(url):

    # This function will unshorten a minified URL and return the original url.
    MAX_REDIRECTS = 10
    retry_attempts = 0

    while True:
        r = requests.head(url)
        if (r.status_code in [301,302]):   # URL appears valid but is a redirect, so continue following redirects
            url = r.headers['location']
        elif str(r.status_code)[:1] == "5":
            wait_time = 2**retry_attempts
            time.sleep(wait_time)
            continue
        elif str(r.status_code)[:1] == "2":  # 2xx response -- this should be the original URL
            return url
        else:
            return None
        retry_attempts += 1
        if retry_attempts == MAX_REDIRECTS:
            return None


print(unshortenURL("https://www.cnn.com"))
