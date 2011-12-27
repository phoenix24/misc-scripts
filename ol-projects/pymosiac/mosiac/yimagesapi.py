import simplejson
import urllib
from google.appengine.api import urlfetch


"""
 YBOSS AppID :
 wRMw7pzV34F7L22s9rVmPbJepd5Dm.PLDd5JiWYYCCTt2a4tpWAl4KwPWfQjs3YAsCI-
 rEgy9FPV34G3Gc5ahFG2H_XeS8G1pAxAMn5N6nSHCWwdcbpes_H6nQHtrX6Gjr0AVA8-
 
 YBOSS URL format:
 http://boss.yahooapis.com/ysearch/images/v1/{query}?appid=xyz
"""

APPID = "wRMw7pzV34F7L22s9rVmPbJepd5Dm.PLDd5JiWYYCCTt2a4tpWAl4KwPWfQjs3YAsCI-"
base_url = "http://boss.yahooapis.com/ysearch/images/v1/%s?appid=%s&format=json"
fetchHeaders = {"User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US; rv:1.8.1) Gecko/20061010 Firefox/2.0", "Accept-encoding": "gzip"}

def fetchImagesURLs(queryKeyword):
    ybossURL = ybossURLPrefix % (queryKeyword, ybossAppID)
    ybossResponse = urllib.urlopen(ybossURL).read()
    ybossResults = simplejson.loads(ybossResponse)['ysearchresponse']['resultset_images']
    return ybossResults

def fetch_search_results_as_json(query, appid = APPID):
    response = fetch_search_results(query, appid = APPID)
    if response.status_code == 200:
        response = simplejson.loads(response.content) 
    else:
        response = "search failed."
    
    return response

def fetch_search_results(query, appid = APPID):
    url = base_url % (query, appid)
    response = urlfetch.fetch(url, headers=fetchHeaders)
    return response