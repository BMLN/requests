from Proxy_List_Scrapper import Scrapper, Proxy, ScrapperException
import requests
from parsel import Selector

import pandas as pd





def get(url, **kwargs):
    content = None
    error = None

    try:
        r = requests.get(
            url, 
            **kwargs
        )

        content = str(r.content)

    except Exception as err:
        error = repr(err)
    
    return content, error


def from_scrapper():

    scrapper = Scrapper(category="ALL", print_err_trace=False)
    data = scrapper.getProxies()

    return pd.DataFrame([ ("proxylistscrapper", x.ip, x.port) for x in data.proxies ], columns=["src", "ip","port"] )


#TODO: better code
def from_geonode():
    __source = """https://proxylist.geonode.com/api/proxy-list?protocols=https%2Chttp&limit=500&page=1&sort_by=lastChecked&sort_type=desc"""
    data = []

    page = requests.get(__source)

    if page:
        data = page.json()["data"]
        
    data = pd.DataFrame(data)
    data["src"] = "geonode"


    return data[["src", "ip", "port"]]


def from_netzwelt():
    __source = """https://www.netzwelt.de/proxy/index.html"""
    data = []
    
    page, error = get(__source)

    if page:
        rows = Selector(page).xpath("""//div[@class="tblc"]//table//tbody//tr""")
        data = [ ["netzwelt"] + row.xpath(".//text()").getall() for row in rows ]

    return pd.DataFrame(data, columns=["src", "ip", "port", "country", "security_level", "type", "FP"])[["src", "ip", "port"]]


def from_hasdata():
    __source = """https://hasdata.com/free-proxy-list"""
    data = []

    page, error = get(__source)

    if page:
        rows = Selector(page).xpath("""//table[@class="richtable"]//tbody//tr""")
        data = [ ["hasdata"] + x.xpath(".//td//text()").getall() for x in rows ]

    return pd.DataFrame(data, columns=["src", "ip", "port", "protocol", "country", "Anonymity",	"Update Time (UTC)"])[["src", "ip", "port"]]


def ipstring(row):
    return str(row["ip"]) + ":" + str(row["port"])



#test for AVAILABILITY(timeout), general block, cloudflare block
def test_proxy(proxy, test_url):
    available = False
    not_blocked = False
    cloudflare = False
    error = None
    
    try:
        r = requests.get(
            test_url, 
            proxies={
                "http" : proxy,
                #"https": proxy #test_both, only http? or get prot from input?
            },
            timeout=20
        )
        page = str(r.content)
        
        available = True
        blocked = "blocked" in page or "banned" in page
        cloudflare = "cloudflare" in page

    except Exception as e:
        error = repr(e)

    return available, not_blocked, cloudflare, error



if __name__ == "__main__":
    
    #inputs
    proxies = []
    proxy_srcs = [from_scrapper, from_geonode, from_netzwelt, from_hasdata]

    for proxy_src in proxy_srcs:
        proxy_list = proxy_src()
        proxies.append(proxy_list)
        print("added " + str(len(proxy_list)) + " proxies")

    proxies = pd.concat(proxies).reset_index()


    #testing
    tests = proxies.apply(ipstring, axis=1).apply(test_proxy, args=("https://google.de",))
    tests = pd.DataFrame(tests.to_list(), columns=["Available", "Blocked", "CloudFlare", "Error"])
    

    #output
    results = pd.concat([proxies, tests], axis=1) #TODO:InvalidINdexError?

    if save := True:
        results.to_csv("./results.csv")


    

#worked:
#117.250.3.58:8080
#112.198.186.77:8082 
#65.1.40.47:1080