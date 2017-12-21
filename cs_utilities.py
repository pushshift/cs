import requests


def unshortenURL(url):

    # This function will unshorten a minified URL and return the original url.
    max_redirects = 10

    while True:
        r = requests.head(url)
        if (r.status_code in [301,302]):   # URL appears valid but is a redirect, so continue following redirects
            url = r.headers['location']
        elif str(r.status_code)[:1] == "5":
            continue
        elif str(r.status_code)[:1] == "2":  # 2xx response -- this should be the original URL
            return url
        else:
            return None
        max_redirects -= 1
        if max_redirects == 0:
            return None

