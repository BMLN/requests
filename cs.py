import requests
import requests_html
import cloudscraper
import pandas as pd

scraper = cloudscraper.create_scraper(debug=True, timeout=2*60)

# blocked
# f = requests.get(
#    "https://google.de",
#    proxies = {"http": "52.66.10.253:80"}
# )

#f = scraper.get("https://www.whatsmyip.org", proxies={"http": "52.66.10.253:80"})
#print(f.text)

proxies = {"http": "http://45.240.182.116:1981" }#, "https": "http://45.240.182.116:1981"}


headers= {
        #"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        #"Accept-Encoding": "gzip, deflate, br",
        #"Host": "de.indeed.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15",
        #"Accept-Language": "de-DE,de;q=0.9",
        #"Referer": "https://de.indeed.com/jobs?q=Werkstudent+IT&vjk=eec87946ee541cd0",
        #"Connection": "keep-alive"
}

# f = requests.get(
#     "http://www.whatsmyip.org",
#     proxies = proxies
# )
# print(f.text)
# exit()
#f = scraper.get("https://www.whatsmyip.org") 
#f = scraper.get("https://de.indeed.com/jobs?q=Rewe")
#f = scraper.get("https://cardmarket.com/de/YuGiOh")
#f = scraper.get("https://www.google.de")
#f = scraper.get("https://stepstone.de/jobs/adidas")



c = 0
d = 0
for job_url in pd.read_csv("indeed_jobs.csv")["url"]:
        for x in range(50000000):
                pass
        print(job_url)

        with scraper.get(job_url) as resp:
                if resp.status_code != 200:
                        if (c - d) > 15: 
                                exit("outt")
                else:
                        if (("""<span id="challenge-error-text">Enable JavaScript and cookies to continue</span>""" in str(resp.content)) == False) and (("""<h1 data-translate="block_headline">Sorry, you have been blocked</h1>""" in str(resp.content)) == False):
                                d += 1
        c += 1
        print("did " + str(d) + " out of " + str(c))
