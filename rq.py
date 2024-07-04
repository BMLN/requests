import requests
import pandas as pd

post_body = {
    "cmd": "request.get",
    #"url": "https://de.indeed.com",
    "url": "https://www.cardmarket.com/de/YuGiOh",
    #"url": "https://nowsecure.nl",
    "maxTimeout": 60000
}


data = pd.read_csv("./indeed_jobs.csv")["url"]
print(data)
print(data[734])
exit()





resp = requests.post(
    "http://localhost:8191/v1",
    headers={"Content-Type": "application/json"},
    json=post_body
)





print(resp.json())
print(resp.content)