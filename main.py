from  crawl import Crawl
from extract import Extract
import pandas as pd
import datetime
from store import Store

class Main(object):
    def __init__(self):
        self.crawl = Crawl()
        self.extract = Extract()

    def __str__(self):
        return '-正在搭建爬取、提取、保存模块-'

    def get_user_info(self,filepath,col_name):
        """
        [{},{}]
        """
        df_user_link = pd.read_excel(filepath)
        list_user_link = df_user_link[col_name].tolist()

        user_info_list = []
        for i, user_link in enumerate(list_user_link, start=1):
            try:
                print(f'-当前进度：[{i}/{len(list_user_link)}] {user_link}')
                page = self.crawl.user_crawl(user_link)
                info = self.extract.user_extract(page, user_link)
                print(f'-提取到的信息：{info}')
                user_info_list.append(info)
            except:
                print('-当前进度存在问题-')
                pass
        store = Store(user_info_list)
        store.store_user_mode_mysql('test_facebook','user_info')

    def get_friends_info(self,filepath,col_name):
        """
        [[{},{}] ,[{},{}]]
        """
        df_friends_link = pd.read_excel(filepath)
        list_friends_link = df_friends_link[col_name].tolist()

        for i, friends_link in enumerate(list_friends_link, start=1):
            print(f"-当前进度：[{i}/{len(list_friends_link)}] 处理{friends_link}")

            has_more = True
            end_cursor = ''
            id = None

            n = 1
            while has_more == True:
                try:
                    print(f"-内部进度：[{n}页]")
                    id, data = self.crawl.friends_crawl(friends_link, end_cursor, id)
                    end_cursor, has_more, info = self.extract.friends_following_followers_extract(data, friends_link)
                    print(f'-提取到的信息：{info}')
                    store = Store(info)
                    store.store_friends_following_followers_mode_mysql('test_facebook', 'friends_info')
                    n += 1
                except:
                    has_more = False
                    print('-当前进度存在问题-')
                    pass

    def get_following_info(self,filepath,col_name):
        """
        [[{},{}] ,[{},{}]]
        """
        df_following_link = pd.read_excel(filepath)
        list_following_link = df_following_link[col_name].tolist()

        for i, following_link in enumerate(list_following_link, start=1):
            print(f"-当前进度：[{i}/{len(list_following_link)}] 处理{following_link}")

            has_more = True
            end_cursor = ''
            id = None

            n = 1
            while has_more == True:
                try:
                    print(f"-内部进度：[{n}页]")
                    id,data = self.crawl.following_crawl(following_link,end_cursor,id)
                    end_cursor, has_more, info = self.extract.friends_following_followers_extract(data, following_link)
                    print(f'-提取到的信息：{info}')
                    store = Store(info)
                    store.store_friends_following_followers_mode_mysql('test_facebook', 'following_info')
                    n += 1
                except:
                    has_more = False
                    print('-当前进度存在问题-')
                    pass
    
    def get_followers_info(self,filepath,col_name):
        """
        [[{},{}] ,[{},{}]]
        """
        df_followers_link = pd.read_excel(filepath)
        list_followers_link = df_followers_link[col_name].tolist()

        for i, followers_link in enumerate(list_followers_link, start=1):
            print(f"-当前进度：[{i}/{len(list_followers_link)}] 处理{followers_link}")

            has_more = True
            end_cursor = ''
            id = None

            n = 1
            while has_more == True:
                try:
                    print(f"-内部进度：[{n}页]")
                    id,data = self.crawl.followers_crawl(followers_link,end_cursor,id)
                    end_cursor, has_more, info = self.extract.friends_following_followers_extract(data, followers_link)
                    print(f'-提取到的信息：{info}')
                    store = Store(info)
                    store.store_friends_following_followers_mode_mysql('test_facebook', 'followers_info')
                    n += 1
                except:
                    has_more = False
                    print('-当前进度存在问题-')
                    pass

    def get_post_info(self,filepath,col_name,start_time='',end_time=''):
        """
        [[{},{}] ,[{},{}]]
        """
        df_post_link = pd.read_excel(filepath)
        list_post_link = df_post_link[col_name].tolist()

        all_post_info_list = []
        for i, post_link in enumerate(list_post_link, start=1):
            print(f"-当前进度：[{i}/{len(list_post_link)}] 处理{post_link}")

            has_more = True
            cursor = ''
            id = None
            crawl_time = True

            temp_post_info_list = []
            n = 1
            while has_more == True:
                if crawl_time:
                    try:
                        print(f"-内部进度：[{n}页]")
                        id,data = self.crawl.post_crawl(post_link,id,cursor,end_time)
                        info, has_more, cursor = self.extract.post_extract(data)
                        print(f'-提取到的信息：{info}')
                        temp_post_info_list.append(info)
                        store = Store(temp_post_info_list)
                        store.store_post_mode_mysql('test_facebook', 'post_info')

                        crawl_time = self.__time_earlier(start_time,info['creation_time'])
                        n += 1
                    except:
                        has_more = False
                        print('-当前进度存在问题-')
                        pass
                else:
                    break
            all_post_info_list.append(temp_post_info_list)
    def __time_earlier(self,start_time,crawl_time):
        crawl_time = datetime.datetime.strptime(crawl_time, "%Y-%m-%d %H:%M:%S")
        if start_time == '':
            return True
        else:
            start_time = datetime.datetime.strptime(start_time, "%y-%m-%d")
            return start_time < crawl_time

if __name__ == '__main__':
    a = Main()

    filepath = '原始用户列表.xlsx'
    col_name = 'userid'

    # b = a.get_user_info(filepath,col_name)

    # c = a.get_friends_info(filepath,col_name)

    # d = a.get_following_info(filepath,col_name)

    # e = a.get_followers_info(filepath,col_name)

    f = a.get_post_info(filepath,col_name)

