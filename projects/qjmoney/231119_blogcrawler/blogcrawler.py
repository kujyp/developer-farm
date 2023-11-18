import requests

url = 'https://blog.naver.com/api/blogs/qjmoney/posts/223268359372/sympathy-users'
headers = {
    'authority': 'blog.naver.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'charset': 'utf-8',
    'content-type': 'application/x-www-form-urlencoded; charset=utf-8',
    'dnt': '1',
    'referer': 'https://blog.naver.com/SympathyHistoryList.naver?blogId=qjmoney&logNo=223268359372&layoutWidthClassName=contw-966%20vsc-initialized',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
}

params = {
    'itemCount': '60',
    'timeStamp': '1700325841890',
}

response = requests.get(url, headers=headers, params=params)

print(response.text)
