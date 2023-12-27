import requests
from bs4 import BeautifulSoup
from lxml import etree

upbit_market_news = []
upbit_new_coin = []


def bithumb_get_market_notices():
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

    for i in range(5):
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        dom = etree.HTML(str(soup))
        targets = dom.xpath('//*[@id="dataTables"]/tbody/tr[*]/td[2]/a')
        ret = []
        
        for target in targets:
            if "[마켓 추가]" in target.text:
                ret.append(target.text)

        print(ret[0])


def upbit_get_market_notices():
    url = "https://api-manager.upbit.com/api/v1/notices?page=1&per_page=20&thread_name=general"
    
    headers = {
    "accept": "application/json",
    "accept-language": "ko-KR, ko;q=1, ko-KR;q=0.1",
    "if-none-match": "W/\"4974fb7aaaced2abde327bed200bebb7\"",
    "sec-ch-ua": "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "Referer": "https://upbit.com/",
    "Referrer-Policy": "origin"
    }   

    response = requests.get(url, headers=headers)

    data = response.json()['data']['list']

    for i in range(len(data)):
        temp = data[i]['title']
        if ("거래" in temp) and ("자산 추가" in temp):
            upbit_market_news.append(temp)
            start_index = upbit_market_news[0].find("(")+1
            end_index = upbit_market_news[0].find(")")

            new_coin = upbit_market_news[0][start_index:end_index]
            # print(upbit_market_news[0][start_index:end_index])
            if new_coin not in upbit_new_coin:
                upbit_new_coin.append(upbit_market_news[0][start_index:end_index])
                print('New coin is just arrived, check this out!')
            else:
                print("Nothing is happened, just old news")

for i in range(5):
    upbit_get_market_notices()
    