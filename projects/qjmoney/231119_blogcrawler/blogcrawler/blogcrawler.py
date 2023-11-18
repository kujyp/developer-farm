import requests
import time


def get_sympathy_users(userid: str, postid: str):
    users = []
    timestamp = int(time.time() * 1000) + 3000

    while True:
        url = f"https://blog.naver.com/api/blogs/{userid}/posts/{postid}/sympathy-users"
        headers = {
            'authority': 'blog.naver.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'charset': 'utf-8',
            'content-type': 'application/x-www-form-urlencoded; charset=utf-8',
            'dnt': '1',
            'referer': f"https://blog.naver.com/SympathyHistoryList.naver?blogId={userid}&logNo={postid}&layoutWidthClassName=contw-966%20vsc-initialized",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
        }

        params = {
            'itemCount': '60',
            'timeStamp': str(timestamp),
        }

        response = requests.get(url, headers=headers, params=params)
        users.extend(response.json()["result"]["users"])
        timestamp = response.json()["result"]["nextTimestamp"]
        if timestamp == -1:
            break
    return users
