import requests
from bs4 import BeautifulSoup
from lxml import etree


def get_market_notices():
    url = "https://cafe.bithumb.com/view/boards/43"

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "sec-ch-ua": "\"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-site",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    dom = etree.HTML(str(soup))
    targets = dom.xpath('//*[@id="dataTables"]/tbody/tr[*]/td[2]/a')
    ret = []
    for target in targets:
        if "[마켓 추가]" in target.text:
            ret.append(target.text)

    return ret
