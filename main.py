from crawl import Crawl
from extract import Extract
import pandas as pd
import datetime
from store import Store


class Main(object):
    def __init__(self):
        self.crawl = Crawl()
        self.extract = Extract()

    def get_user_info(self, filepath, col_name):
        """
        Extract user information from a list of URLs in an Excel file.

        Parameters:
        filepath (str): Path to the Excel file.
        col_name (str): Column name containing the URLs.

        Returns:
        None
        """
        df_user_link = pd.read_excel(filepath)
        list_user_link = df_user_link[col_name].tolist()

        user_info_list = []
        for i, user_link in enumerate(list_user_link, start=1):
            try:
                print(f'-Current progress: [{i}/{len(list_user_link)}] {user_link}')
                page = self.crawl.user_crawl(user_link)
                info = self.extract.user_extract(page, user_link)
                print(f'-Extracted information: {info}')
                user_info_list.append(info)
            except:
                print('-Current progress encountered an issue-')
                pass
        store = Store(user_info_list)
        store.store_user_mode_mysql('test_facebook', 'user_info')

    def get_friends_info(self, filepath, col_name):
        """
        Extract friends information from a list of URLs in an Excel file.

        Parameters:
        filepath (str): Path to the Excel file.
        col_name (str): Column name containing the URLs.

        Returns:
        None
        """
        df_friends_link = pd.read_excel(filepath)
        list_friends_link = df_friends_link[col_name].tolist()

        for i, friends_link in enumerate(list_friends_link, start=1):
            print(f"-Current progress: [{i}/{len(list_friends_link)}] Processing {friends_link}")

            has_more = True
            end_cursor = ''
            id = None

            n = 1
            while has_more:
                try:
                    print(f"-Internal progress: [{n} page]")
                    id, data = self.crawl.friends_crawl(friends_link, end_cursor, id)
                    end_cursor, has_more, info = self.extract.friends_following_followers_extract(data, friends_link)
                    print(f'-Extracted information: {info}')
                    store = Store(info)
                    store.store_friends_following_followers_mode_mysql('test_facebook', 'friends_info')
                    n += 1
                except:
                    has_more = False
                    print('-Current progress encountered an issue-')
                    pass

    def get_following_info(self, filepath, col_name):
        """
        Extract following information from a list of URLs in an Excel file.

        Parameters:
        filepath (str): Path to the Excel file.
        col_name (str): Column name containing the URLs.

        Returns:
        None
        """
        df_following_link = pd.read_excel(filepath)
        list_following_link = df_following_link[col_name].tolist()

        for i, following_link in enumerate(list_following_link, start=1):
            print(f"-Current progress: [{i}/{len(list_following_link)}] Processing {following_link}")

            has_more = True
            end_cursor = ''
            id = None

            n = 1
            while has_more:
                try:
                    print(f"-Internal progress: [{n} page]")
                    id, data = self.crawl.following_crawl(following_link, end_cursor, id)
                    end_cursor, has_more, info = self.extract.friends_following_followers_extract(data, following_link)
                    print(f'-Extracted information: {info}')
                    store = Store(info)
                    store.store_friends_following_followers_mode_mysql('test_facebook', 'following_info')
                    n += 1
                except:
                    has_more = False
                    print('-Current progress encountered an issue-')
                    pass

    def get_followers_info(self, filepath, col_name):
        """
        Extract followers information from a list of URLs in an Excel file.

        Parameters:
        filepath (str): Path to the Excel file.
        col_name (str): Column name containing the URLs.

        Returns:
        None
        """
        df_followers_link = pd.read_excel(filepath)
        list_followers_link = df_followers_link[col_name].tolist()

        for i, followers_link in enumerate(list_followers_link, start=1):
            print(f"-Current progress: [{i}/{len(list_followers_link)}] Processing {followers_link}")

            has_more = True
            end_cursor = ''
            id = None

            n = 1
            while has_more:
                try:
                    print(f"-Internal progress: [{n} page]")
                    id, data = self.crawl.followers_crawl(followers_link, end_cursor, id)
                    end_cursor, has_more, info = self.extract.friends_following_followers_extract(data, followers_link)
                    print(f'-Extracted information: {info}')
                    store = Store(info)
                    store.store_friends_following_followers_mode_mysql('test_facebook', 'followers_info')
                    n += 1
                except:
                    has_more = False
                    print('-Current progress encountered an issue-')
                    pass

    def get_post_info(self, filepath, col_name, start_time='', end_time=''):
        """
        Extract post information from a list of URLs in an Excel file.

        Parameters:
        filepath (str): Path to the Excel file.
        col_name (str): Column name containing the URLs.
        start_time (str, optional): Start time for filtering posts. Defaults to ''.
        end_time (str, optional): End time for filtering posts. Defaults to ''.

        Returns:
        None
        """
        df_post_link = pd.read_excel(filepath)
        list_post_link = df_post_link[col_name].tolist()

        all_post_info_list = []
        for i, post_link in enumerate(list_post_link, start=1):
            print(f"-Current progress: [{i}/{len(list_post_link)}] Processing {post_link}")

            has_more = True
            cursor = ''
            id = None
            crawl_time = True

            temp_post_info_list = []
            n = 1
            while has_more:
                if crawl_time:
                    try:
                        print(f"-Internal progress: [{n} page]")
                        id, data = self.crawl.post_crawl(post_link, id, cursor, end_time)
                        info, has_more, cursor = self.extract.post_extract(data)
                        print(f'-Extracted information: {info}')
                        temp_post_info_list.append(info)
                        store = Store(temp_post_info_list)
                        store.store_post_mode_mysql('test_facebook', 'post_info')

                        crawl_time = self.__time_earlier(start_time, info['creation_time'])
                        n += 1
                    except:
                        has_more = False
                        print('-Current progress encountered an issue-')
                        pass
                else:
                    break
            all_post_info_list.append(temp_post_info_list)

    def __time_earlier(self, start_time, crawl_time):
        """
        Check if the crawl time is earlier than the start time.

        Parameters:
        start_time (str): Start time for comparison.
        crawl_time (str): Crawl time to be compared.

        Returns:
        bool: True if crawl time is earlier than start time, False otherwise.
        """
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

    # a.get_user_info(filepath, col_name)
    # a.get_friends_info(filepath, col_name)
    # a.get_following_info(filepath, col_name)
    # a.get_followers_info(filepath, col_name)
    # a.get_post_info(filepath, col_name)
