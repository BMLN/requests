import requests
import requests_html
import cloudscraper
import pandas as pd

from test import test



def cs_get(url):
    output = requests.Response()
    output.status_code = 500
    output._text=""
    output.url=""
    
    for x in range(100000000): #<-- lol
        pass
    try:
        with scraper.get(url, timeout=2*60) as resp:
            output.status_code = resp.status_code
            output._text = str(resp.content)
            output.url = resp.url
    except:
        pass

    return output

def cs_eval(response):
    url_eval = 1
    status_eval = 1
    challenge_eval = 1
    block_eval = 1

    if ("indeed" in response.url) == False: ##should be https://de.indeed.com, right?
        url_eval = 0
    if (response.status_code != 200):
        status_eval = 0
    if ("""<span id="challenge-error-text">Enable JavaScript and cookies to continue</span>""" in response.text):
        challenge_eval = 0
    if ("""<h1 data-translate="block_headline">Sorry, you have been blocked</h1>""" in response.text):
        block_eval = 0

    return (url_eval, status_eval, challenge_eval, block_eval)








scraper = cloudscraper.create_scraper(debug=True)
data = pd.read_csv("indeed_jobs.csv")["url"]
tester = cs_get
evaler = cs_eval



headers= {
        #"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        #"Accept-Encoding": "gzip, deflate, br",
        #"Host": "de.indeed.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15",
        #"Accept-Language": "de-DE,de;q=0.9",
        #"Referer": "https://de.indeed.com/jobs?q=Werkstudent+IT&vjk=eec87946ee541cd0",
        #"Connection": "keep-alive"
}



test(
    data,
    tester,
    evaler,
    False,
    False
)