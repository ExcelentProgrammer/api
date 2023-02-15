import requests
from uuid import uuid4
import pickle
import re
import json


class Convertor:

    def __init__(self):
        self.headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "uz,en;q=0.9,ru;q=0.8",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "sec-ch-ua": '"Chromium";v="106", "Yandex";v="22", "Not;A=Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-requested-with": "XMLHttpRequest",
            "Referer": "https://developers.convertio.co/user/registration/api?utm_source=api_top_btn",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }

    def request(self, url, files=None, data=None, headers=None, method="POST", cookies=None):

        if headers is None:
            headers = self.headers
        if method == "POST":
            return requests.post(url=url, headers=headers, data=data, files=files, cookies=cookies)
        elif method == "GET":
            return requests.get(url=url, headers=headers, files=files, cookies=cookies)
        else:
            return "In valid method"

    def login(self):
        url = "https://developers.convertio.co/user/confirm/"
        email = uuid4()
        data = {
            "source": "api",
            "email": f"{email}@gmail.com",
            "password": "Samandar001@",
        }
        res = self.request(url, data=data)
        if res.json()['msg'] == "OK":
            with open("cookies", "wb") as file:
                pickle.dump(res.cookies, file)
            return True
        return False

    def getToken(self):
        self.login()
        url = "https://developers.convertio.co/"
        with open("cookies", "rb") as file:
            cookies = pickle.load(file)
            res = self.request(url, cookies=cookies)
            r = re.findall(
                r'<input id="api_input" type="text" onClick="this.select\(\);" value="(.*)" readonly="readonly" style="float:left; width:75%"/>',
                res.text)
            return r[0]
