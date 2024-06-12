import json

import requests
import re
from datetime import datetime
import time

class Crawl(object):

    def user_crawl(self,url):
        cookies,headers = self.__user_setting()
        resp = requests.get(url, cookies=cookies, headers=headers)
        return resp.text

    def __user_setting(self):
        self.cookies = {
            'sb': 'gWVJZm-1I8usm1e8btXEpv2f',
            'datr': 'gWVJZqROEYbyiKkplq-Vwwdd',
            'dpr': '1.25',
            'c_user': '61553712069078',
            'xs': '11%3AaCIlVbpwVqAttQ%3A2%3A1716086153%3A-1%3A-1',
            'fr': '0QSVD2qOMH89jBNX6.AWXasL_LJ4dGDDD75yZKQVbE6eQ.BmSWWB..AAA.0.0.BmSWWK.AWUfc8fsbJ8',
            'ps_n': '1',
            'ps_l': '1',
            'presence': 'C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1716086684454%2C%22v%22%3A1%7D',
            'wd': '1018x695',
        }
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'dpr': '1.25',
            'priority': 'u=0, i',
            'sec-ch-prefers-color-scheme': 'light',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-full-version-list': '"Chromium";v="124.0.6367.208", "Google Chrome";v="124.0.6367.208", "Not-A.Brand";v="99.0.0.0"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"15.0.0"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'viewport-width': '1018',
        }
        return self.cookies,self.headers

    def friends_crawl(self, url ,end_cursor='',id=None):
        if id == None:
            cookies, headers = self.__friends_id_setting()
            if "profile.php?id=" in url:
                url_parts = url.split("?")
                profile_id = url_parts[1].split("=")[1]
                new_url = f"https://www.facebook.com/profile.php?id={profile_id}&sk=friends_all"
            else:
                new_url = url + '/friends_all'
            resp = requests.get(new_url, cookies=cookies, headers=headers)
            ex = '"collectionToken":"(.*?)"'
            id = re.findall(ex, resp.text, re.S)[0]
        else:
            pass
        cookies,headers,params = self.__friends_following_followers_setting(end_cursor,id)
        resp = requests.post('https://www.facebook.com/api/graphql/',cookies=cookies,headers=headers,params=params)
        return id , resp.text

    def __friends_id_setting(self):
        self.cookies = {
            'sb': 'gWVJZm-1I8usm1e8btXEpv2f',
            'datr': 'gWVJZqROEYbyiKkplq-Vwwdd',
            'dpr': '1.25',
            'c_user': '61553712069078',
            'ps_n': '1',
            'ps_l': '1',
            'xs': '11%3AaCIlVbpwVqAttQ%3A2%3A1716086153%3A-1%3A-1%3A%3AAcUScBAqXdAVHCjMq1t3EwA-RV6IkQsg3nf1i01m1cI',
            'fr': '1QDwmpBA3kzZXb32I.AWUB6LeT18Q06HXinTbaifljvkY.BmUCUv..AAA.0.0.BmUCUv.AWUCCEl-1w4',
            'wd': '1019x695',
            'presence': 'C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1716533773560%2C%22v%22%3A1%7D',
        }
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'dpr': '1.25',
            'priority': 'u=0, i',
            'sec-ch-prefers-color-scheme': 'light',
            'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'sec-ch-ua-full-version-list': '"Google Chrome";v="125.0.6422.76", "Chromium";v="125.0.6422.76", "Not.A/Brand";v="24.0.0.0"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"15.0.0"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'viewport-width': '1019',
        }

        return self.cookies,self.headers

    def following_crawl(self, url ,end_cursor='',id=None):
        if id == None:
            cookies, headers = self.__following_id_setting()
            if "profile.php?id=" in url:
                url_parts = url.split("?")
                profile_id = url_parts[1].split("=")[1]
                new_url = f"https://www.facebook.com/profile.php?id={profile_id}&sk=following"
            else:
                new_url = url + '/following'
            resp = requests.get(new_url, cookies=cookies, headers=headers)
            ex = '"collectionToken":"(.*?)"'
            id = re.findall(ex, resp.text, re.S)[0]
        else:
            pass
        cookies,headers,params = self.__friends_following_followers_setting(end_cursor,id)
        resp = requests.post('https://www.facebook.com/api/graphql/',cookies=cookies,headers=headers,params=params)
        return id , resp.text

    def __following_id_setting(self):
        self.cookies = {
            'sb': 'gWVJZm-1I8usm1e8btXEpv2f',
            'datr': 'gWVJZqROEYbyiKkplq-Vwwdd',
            'dpr': '1.25',
            'c_user': '61553712069078',
            'ps_n': '1',
            'ps_l': '1',
            'xs': '11%3AaCIlVbpwVqAttQ%3A2%3A1716086153%3A-1%3A-1%3A%3AAcXI-V_JWaEd7nOAuc7glVk3C_D2oBCrjuge1uLQWQ',
            'fr': '1ZAxgbBShthRxand1.AWUxbaEUHTMkkyfuc5D2KXrKw_4.BmS2GK..AAA.0.0.BmS2GK.AWVFtODsseg',
            'wd': '1019x695',
            'presence': 'C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1716216396722%2C%22v%22%3A1%7D',
        }
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'dpr': '1.25',
            'priority': 'u=0, i',
            'sec-ch-prefers-color-scheme': 'light',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-full-version-list': '"Chromium";v="124.0.6367.208", "Google Chrome";v="124.0.6367.208", "Not-A.Brand";v="99.0.0.0"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"15.0.0"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'viewport-width': '1019',
        }
        return self.cookies,self.headers

    def followers_crawl(self, url ,end_cursor='',id=None):
        if id == None:
            cookies, headers = self.__followers_id_setting()
            if "profile.php?id=" in url:
                url_parts = url.split("?")
                profile_id = url_parts[1].split("=")[1]
                new_url = f"https://www.facebook.com/profile.php?id={profile_id}&sk=followers"
            else:
                new_url = url + '/followers'
            resp = requests.get(new_url, cookies=cookies, headers=headers)
            ex = '"collectionToken":"(.*?)"'
            id = re.findall(ex, resp.text, re.S)[0]
        else:
            pass
        cookies,headers,params = self.__friends_following_followers_setting(end_cursor,id)
        resp = requests.post('https://www.facebook.com/api/graphql/',cookies=cookies,headers=headers,params=params)
        return id , resp.text

    def __followers_id_setting(self):
        self.cookies = {
            'sb': 'gWVJZm-1I8usm1e8btXEpv2f',
            'datr': 'gWVJZqROEYbyiKkplq-Vwwdd',
            'dpr': '1.25',
            'c_user': '61553712069078',
            'ps_n': '1',
            'ps_l': '1',
            'xs': '11%3AaCIlVbpwVqAttQ%3A2%3A1716086153%3A-1%3A-1%3A%3AAcXI-V_JWaEd7nOAuc7glVk3C_D2oBCrjuge1uLQWQ',
            'fr': '1ZAxgbBShthRxand1.AWUxbaEUHTMkkyfuc5D2KXrKw_4.BmS2GK..AAA.0.0.BmS2GK.AWVFtODsseg',
            'wd': '1019x695',
            'presence': 'C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1716216396722%2C%22v%22%3A1%7D',
        }
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'dpr': '1.25',
            'priority': 'u=0, i',
            'sec-ch-prefers-color-scheme': 'light',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-full-version-list': '"Chromium";v="124.0.6367.208", "Google Chrome";v="124.0.6367.208", "Not-A.Brand";v="99.0.0.0"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"15.0.0"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'viewport-width': '1019',
        }
        return self.cookies,self.headers

    def __friends_following_followers_setting(self,page,id):
        self.cookies = {
            'sb': 'gWVJZm-1I8usm1e8btXEpv2f',
            'datr': 'gWVJZqROEYbyiKkplq-Vwwdd',
            'dpr': '1.25',
            'c_user': '61553712069078',
            'ps_n': '1',
            'ps_l': '1',
            'xs': '11%3AaCIlVbpwVqAttQ%3A2%3A1716086153%3A-1%3A-1%3A%3AAcUScBAqXdAVHCjMq1t3EwA-RV6IkQsg3nf1i01m1cI',
            'fr': '1QDwmpBA3kzZXb32I.AWUB6LeT18Q06HXinTbaifljvkY.BmUCUv..AAA.0.0.BmUCUv.AWUCCEl-1w4',
            'wd': '1536x695',
            'presence': 'C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1716529662324%2C%22v%22%3A1%7D',
        }
        self.headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            # 'cookie': 'sb=gWVJZm-1I8usm1e8btXEpv2f; datr=gWVJZqROEYbyiKkplq-Vwwdd; dpr=1.25; c_user=61553712069078; ps_n=1; ps_l=1; xs=11%3AaCIlVbpwVqAttQ%3A2%3A1716086153%3A-1%3A-1%3A%3AAcUScBAqXdAVHCjMq1t3EwA-RV6IkQsg3nf1i01m1cI; fr=1QDwmpBA3kzZXb32I.AWUB6LeT18Q06HXinTbaifljvkY.BmUCUv..AAA.0.0.BmUCUv.AWUCCEl-1w4; wd=1536x695; presence=C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1716529662324%2C%22v%22%3A1%7D',
            'origin': 'https://www.facebook.com',
            'priority': 'u=1, i',
            'referer': 'https://www.facebook.com/rodrigojrbarliso.pacunla/friends',
            'sec-ch-prefers-color-scheme': 'light',
            'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'sec-ch-ua-full-version-list': '"Google Chrome";v="125.0.6422.76", "Chromium";v="125.0.6422.76", "Not.A/Brand";v="24.0.0.0"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"15.0.0"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'x-asbd-id': '129477',
            'x-fb-friendly-name': 'ProfileCometAppCollectionListRendererPaginationQuery',
            'x-fb-lsd': 'yH27yfqRrngPvHuCvAc3q6',
        }
        self.data = {
            'av': '61553712069078',
            '__aaid': '0',
            '__user': '61553712069078',
            '__a': '1',
            '__req': '1q',
            '__hs': '19867.HYP:comet_pkg.2.1..2.1',
            'dpr': '1',
            '__ccg': 'EXCELLENT',
            '__rev': '1013737018',
            '__s': 's9knme:vg3v8s:8mipmh',
            '__hsi': '7372433480073385259',
            '__dyn': '7AzHK4HwkEng5K8G6EjBAg2owIxu13wFwhUngS3q2ibwNwnof8boG0x8bo6u3y4o2Gwfi0LVEtwMw65xO2OU7m221Fwgo9oO0-E4a3a4oaEnxO0Bo7O2l2Utwwwi831wiE567Udo5qfK0zEkxe2GewyAG1jxS6FobrwKxm5oe8464-5pUfEe88o4Wm7-2K0SEuBwFKq2-azo2NwwwOg2cwMwhEkxebwHwNxe6Uak0zU8oC1hxB0qo4e16wWwjHDzUiwRxW1fy8bU',
            '__csr': 'gvNIheQzjjj88YZIyQx4PK_aDGyrnYIDEBvXlhr7YyRQ_Akyb9q9sT99cADRvqmykh6hdaJTGVkilA-y6FGFpogFqXlqDhBBCGdgFeqp2bhbyHCvy4qFQmqECnUyt4x9Km8KXWgC9y4F6ay8W8CKaypHxKext4CwDxWhamaABiUjzoK4rByEK9xOfAy9E988pU43x-aDwxwqUe8422i7U9ElxCU4W4UjUeVEow9W5E88bK0T8bU5a6E6i7awey0ge1Aw5Txydw2Ko5p0eS0e_w6YwRwgo01kve0LA0axwiBAy4bw0GrwZwfK0f0w0Tkwfu0eMw0hRk06j8K361jwl8mo13o4a06qU',
            '__comet_req': '15',
            'fb_dtsg': 'NAcMBHrk_HCKMfzyFV1Ma40hci70FIBuIQi8YRHy2BjZxUyAhIjmZzA:11:1716086153',
            'jazoest': '25408',
            'lsd': 'yH27yfqRrngPvHuCvAc3q6',
            '__spin_r': '1013737018',
            '__spin_b': 'trunk',
            '__spin_t': '1716528432',
            '__jssesw': '1',
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'ProfileCometAppCollectionListRendererPaginationQuery',
            'variables': f'{{"count":8,"cursor": "{page}","scale": 1,"search": null,"id": "{id}"}}',
            'server_timestamps': 'true',
            'doc_id': '8023840227643650',
        }
        return self.cookies,self.headers,self.data

    def post_crawl(self,url,id=None,cursor='',bef_time=''):
        if id == None:
            cookies, headers = self.__followers_id_setting()
            resp = requests.get(url, cookies=cookies, headers=headers).text
            id = re.search('"userID":"(.*?)"', resp, re.S).group(1)
        else:
            pass
        if bef_time == '':
            timestamp = int(time.time()) + 86400
        else:
            date_object = datetime.strptime(bef_time, "%Y-%m-%d")
            timestamp = int(time.mktime(date_object.timetuple())) + 86400

        cookies,headers,params = self.__post_setting(id,cursor,timestamp)

        res = requests.post('https://www.facebook.com/api/graphql/', cookies=cookies, headers=headers, data=params).text
        tate = res.split('\r\n')[0]
        return id,tate

    def __post_id_setting(self):
        self.cookies = {
            'sb': 'gWVJZm-1I8usm1e8btXEpv2f',
            'datr': 'gWVJZqROEYbyiKkplq-Vwwdd',
            'dpr': '1.25',
            'c_user': '61553712069078',
            'xs': '11%3AaCIlVbpwVqAttQ%3A2%3A1716086153%3A-1%3A-1',
            'fr': '0QSVD2qOMH89jBNX6.AWXasL_LJ4dGDDD75yZKQVbE6eQ.BmSWWB..AAA.0.0.BmSWWK.AWUfc8fsbJ8',
            'ps_n': '1',
            'ps_l': '1',
            'presence': 'C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1716086684454%2C%22v%22%3A1%7D',
            'wd': '1018x695',
        }
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'dpr': '1.25',
            'priority': 'u=0, i',
            'sec-ch-prefers-color-scheme': 'light',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-full-version-list': '"Chromium";v="124.0.6367.208", "Google Chrome";v="124.0.6367.208", "Not-A.Brand";v="99.0.0.0"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"15.0.0"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'viewport-width': '1018',
        }
        return self.cookies,self.headers

    def __post_setting(self,id,cursor,time):
        self.cookies = {
            'sb': 'gWVJZm-1I8usm1e8btXEpv2f',
            'datr': 'gWVJZqROEYbyiKkplq-Vwwdd',
            'dpr': '1.25',
            'c_user': '61553712069078',
            'ps_n': '1',
            'ps_l': '1',
            'wd': '1019x695',
            'xs': '11%3AaCIlVbpwVqAttQ%3A2%3A1716086153%3A-1%3A-1%3A%3AAcUScBAqXdAVHCjMq1t3EwA-RV6IkQsg3nf1i01m1cI',
            'fr': '1QDwmpBA3kzZXb32I.AWUB6LeT18Q06HXinTbaifljvkY.BmUCUv..AAA.0.0.BmUCUv.AWUCCEl-1w4',
            'presence': 'C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1716528439127%2C%22v%22%3A1%7D',
        }
        self.headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.facebook.com',
            'priority': 'u=1, i',
            'referer': 'https://www.facebook.com/rodrigojrbarliso.pacunla',
            'sec-ch-prefers-color-scheme': 'light',
            'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'sec-ch-ua-full-version-list': '"Google Chrome";v="125.0.6422.76", "Chromium";v="125.0.6422.76", "Not.A/Brand";v="24.0.0.0"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"15.0.0"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'x-asbd-id': '129477',
            'x-fb-friendly-name': 'ProfileCometTimelineFeedRefetchQuery',
            'x-fb-lsd': 'yH27yfqRrngPvHuCvAc3q6',
        }
        self.data = {
            'av': '61553712069078',
            '__aaid': '0',
            '__user': '61553712069078',
            '__a': '1',
            '__req': 'j',
            '__hs': '19867.HYP:comet_pkg.2.1..2.1',
            'dpr': '1',
            '__ccg': 'EXCELLENT',
            '__rev': '1013737018',
            '__s': 'wz8j5n:vg3v8s:8mipmh',
            '__hsi': '7372433480073385259',
            '__dyn': '7AzHK4HwkEng5K8G6EjBAg2owIxu13wFwhUngS3q2ibwNwnof8boG0x8bo6u3y4o2Gwfi0LVEtwMw65xO2OU7m221Fwgo9oO0-E4a3a4oaEnxO0Bo7O2l2Utwwwi831wiE567Udo5qfK0zEkxe2GewyAG1jxS6FobrwKxm5oe8464-5pUfEe88o4Wm7-2K0SEuBwFKq2-azo2NwwwOg2cwMwhEkxebwHwNxe6Uak0zU8oC1hxB0qo4e16wWwjHDzUiwRxW1fy8bU',
            '__csr': 'gvNIheQznkQO2ffp6J8hcXLOFWECR_b9W9n-Ri4r7IyRVfAlqb9rqlnOmz99ZnSBEB4hAjiHtWKl4BpbExGqGm5GmKRmFQvBCGdzbCCgyQiUGVDyA4kmqECnUyt4x9Km8KXWgC9y4F6ay8W8CKaypHxKext4CwDxWhamfBiUjzoK4rBxq9xOfAy9E988pU43x-aDwxwqUe86m7U9ElxCU4W4UjwZCxy0DEmwwwKU3swLwkEqwp8sG0uO1Aw5TwCw2Ko5p0eS0e_w6YwtU01kve0LA0axwiBAy4bw0GrwZwfK0f0w0Tkwfu0eMw0o8UK081wgE0pHw',
            '__comet_req': '15',
            'fb_dtsg': 'NAcMBHrk_HCKMfzyFV1Ma40hci70FIBuIQi8YRHy2BjZxUyAhIjmZzA:11:1716086153',
            'jazoest': '25408',
            'lsd': 'yH27yfqRrngPvHuCvAc3q6',
            '__spin_r': '1013737018',
            '__spin_b': 'trunk',
            '__spin_t': '1716528432',
            '__jssesw': '1',
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'ProfileCometTimelineFeedRefetchQuery',
            'variables': f'{{"afterTime":null,"beforeTime":{time},"count":3,"cursor":"{cursor}","feedLocation":"TIMELINE","feedbackSource":0,"focusCommentID":null,"memorializedSplitTimeFilter":null,"omitPinnedPost":true,"postedBy":null,"privacy":null,"privacySelectorRenderLocation":"COMET_STREAM","renderLocation":"timeline","scale":1,"stream_count":1,"taggedInOnly":null,"useDefaultActor":false,"id":"{id}","__relay_internal__pv__CometImmersivePhotoCanUserDisable3DMotionrelayprovider":false,"__relay_internal__pv__IsWorkUserrelayprovider":false,"__relay_internal__pv__IsMergQAPollsrelayprovider":false,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false,"__relay_internal__pv__CometUFIShareActionMigrationrelayprovider":false,"__relay_internal__pv__CometIsAdaptiveUFIEnabledrelayprovider":false,"__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider":false,"__relay_internal__pv__StoriesRingrelayprovider":false,"__relay_internal__pv__EventCometCardImage_prefetchEventImagerelayprovider":true}}',
            'server_timestamps': 'true',
            'doc_id': '26470356505897296',
        }
        return self.cookies,self.headers,self.data

if __name__ == '__main__':
    a = Crawl()
    b = a.user_crawl('https://www.facebook.com/emyrrej.artsal')
    # print(b)

    # c = a.friends_crawl('https://www.facebook.com/profile.php?id=100050249863966')
    # print(c[0])

    c = a.followers_crawl('https://www.facebook.com/profile.php?id=100050249863966')
    print(c[0])

    c = a.following_crawl('https://www.facebook.com/profile.php?id=100050249863966')
    print(c[0])

    # from extract import Extract
    # d = Extract()
    # e = d.friends_following_followers_extract(c[1],'https://www.facebook.com/profile.php?id=100050249863966')
    # print(e)

    # c = a.post_crawl('https://www.facebook.com/emyrrej.artsal',cursor='AQHR1ThKwoJjDSqEmkcRCuk78tXPNiSMgPk7My5GPPhAS9StcSrOZ_pBMuxeICZmxq4CZXPpTSoL3fnHGK8Db75j088iNQpsnlJlZap_0k5nrGJuJERXPTJfKSQm50xEx7zn4J-3C66bbQYLTysayREnUKqn2cjefbfO1paXlQ3VA2Tq68vANJF6TpJN41kKvt8QjfcIXYJ2xAfPglcqFdxaMti-l8ovnUUk4zxPixodJN_oYjiCjnFTFuFpoG8o5I7wZntAyBt9F6fKlIeXztWTftPpwDfxn8Ltn0_FJFVA1kbz4bGAKqrAKREB8-xwKZImltO25-LQ5JfUzY5cxhA8yyJYZTF2hE-dffDCJOaLjlHc1s1YcK7F2Cz26W4kctW4_89dSKQPGfXyFDyBv64jNKNhpzaFE8m9-i1MsXJsnp7YzPsZ86w6bGoP8dyRUqK2f0B0XF3yISOKnpZLSt4lBw')
    # print(c[1])
    #
    # from extract import Extract
    # d = Extract()
    # e = d.post_extract(json.loads(c[1]))
    # print(e)

