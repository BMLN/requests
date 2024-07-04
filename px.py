import requests


ip = "173.249.37.45"
ip = "49.13.252.196"
port = "5005"
port = "80"

proxies = {
    "http" : "http://{}:{}".format(ip, port),
    "https" : "http://{}:{}".format(ip, port)
}

with requests.get("http://whatsmyip.com", proxies=proxies) as req:

    print(req.text)
    print(req.status_code)