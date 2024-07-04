import requests
from parsel import Selector

import pandas as pd
import time

def get(url, **kwargs):
    content = None
    error = None

    try:
        r = requests.get(
            url, 
            **kwargs
        )
        time.sleep(5)
        content = str(r.content)

    except Exception as err:
        error = repr(err)
    
    return content, error


#javascript :()
def __extract_freeproxyworld_page(pagecontent) -> list[tuple]:
    output = [] # ["ips", "ports", "countries", "cities", "speeds"]}
    #output_next = None
     
    selector = Selector(pagecontent)

    for row in selector.xpath("""//div[@class="proxy-table"]//tr"""):
        print(selector.xpath("""//div[@class="proxy-table"]""").getall())
        exit()
        print(row)
        if (columns := row.xpath(".//td")):
            print("yyy")
            ip = "".join(columns[0].xpath(".//text()").getall()).replace("\n", "").replace("\r", "").replace(" ", "")
            port = "".join(columns[1].xpath(".//text()").getall()).replace("\n", "").replace("\r", "").replace(" ", "")
            country = "".join(columns[2].xpath(".//text()").getall()).replace("\n", "").replace("\r", "").replace(" ", "")
            city = "".join(columns[3].xpath(".//text()").getall()).replace("\n", "").replace("\r", "").replace(" ", "")
            speed = "".join(columns[4].xpath(".//text()").getall()).replace("\n", "").replace("\r", "").replace(" ", "")
            
            output.append(
                (
                    ip, port, country, city, speed
                )
            )

    #output_next = selector.xpath("""//div[@class="proxy_table_pages"]//@data-counts""")
    #return output_data, output_next
    print("lists", len(output))
    return output 

def __extract_freeproxyworld_total(pagecontent):
    return Selector(pagecontent).xpath("""//div[@class="proxy_table_pages"]//@data-counts""")


def from_freeproxyworld():
    __sources = [
        """https://www.freeproxy.world/?type=https&country=DE""",
        """https://www.freeproxy.world/?type=http&country=DE"""
    ]

    output = []

    for src in __sources:
        page_addr = src
        total_data = 0
        page_nr = 1
        src_output = [] 
        
        while (page_addr != None):
            page = get(page_addr)
            page_addr = None

            if (page := page[0]):
                if total_data == 0: total_data = __extract_freeproxyworld_total(page)
                src_output += __extract_freeproxyworld_page(page)
                
                if src_output < total_data:
                    page_addr = src + "&page=" + str(page_nr := page_nr + 1)
            print(len(src_output))

        output += src_output
        
    return output
    output["src"] = [ "freeproxyworld" ] * len(output["ips"])

    #return pd.DataFrame(output)[["src", "ips", "port"]]




def from_geonode():
    __source = """https://proxylist.geonode.com/api/proxy-list?protocols=https%2Chttp&limit=500&page=1&sort_by=lastChecked&sort_type=desc"""
    data = pd.DataFrame()

    data = requests.get(__source).json()
    print(data)

    if data:
        data = pd.DataFrame(data["data"])[["ip", "port"]]
        data["src"] = "geonode"

    return data


import json
if __name__ == "__main__":
    # f = open("./freeproxyworld.html", "r")

    # sel = Selector(text=f.read())
    # #sel = sel.xpath("""//div[@class="proxy-table"]//tr""")

    # t = sel.xpath("""//div[@class="proxy_table_pages"]""")
    # print(t.getall())
    # print(t.xpath("""//span[@class="layui-laypage-curr"]"""))

    # print("run")
    # if (page := get("""https://www.freeproxy.world/?type=http&country=DE""")[0]):
    #     print("got")
    #     __extract_freeproxyworld_page(page)
    print(from_geonode())