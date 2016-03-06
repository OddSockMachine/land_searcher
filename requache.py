import requests
import redislite

redis = redislite.StrictRedis("./redis.db")

def get(url):
    cached = redis.get(url)
    if cached:
        # url found in cache
        return cached
    # not found, getting
    req  = requests.get(url)
    text = req.text
    redis.set(url, text)
    return text
