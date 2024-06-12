import pymysql

class Store(object):
    """
    Store is a class designed to store extracted data into MySQL and Excel.

    Methods:
        mode_mysql(db_name, tb_name): Stores data into a MySQL database.
        mode_excel(excel_name): Stores data into an Excel file.
    """

    def __init__(self, data_list):
        """
        Initializes the Store class with a list of data.

        Args:
            data_list (list): The list of data to store.
        """
        self.data_list = data_list

    def store_user_mode_mysql(self, db_name, tb_name):
        """
        Stores data into a MySQL database.

        Args:
            db_name (str): The name of the database.
            tb_name (str): The name of the table.
        """
        try:
            # 连接数据库
            self.db = pymysql.connect(host='localhost', user='root', passwd='wz131', port=3306)
            self.cursor = self.db.cursor()
            print('-连接成功-')

            # 检查并创建数据库（如果不存在）
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            print('-数据库已检查-')

            # 选择数据库
            self.cursor.execute(f"USE {db_name}")

            # 创建数据表
            self.__create_user_table(tb_name)

            # 插入数据
            self.__user_insert(tb_name)
            # print('-正在插入数据-')

            # 关闭mysql
            self.db.close()
            print('-连接关闭-')

        except pymysql.MySQLError as e:
            print(f"连接数据库时出现错误：{e}")

    def __create_user_table(self, tb_name):
        """
        Creates a table in the MySQL database if it doesn't exist.

        Args:
            tb_name (str): The name of the table.
        """
        try:
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {tb_name} (
                MAIN_ID INT AUTO_INCREMENT PRIMARY KEY,
                账号url Text,
                账号ID Text,
                账号昵称 Text,
                性别 VARCHAR(50),
                关系状况 Text,
                个人描述 Text
            );
            """
            self.cursor.execute(create_table_query)
            print('-表已检查-')

        except pymysql.MySQLError as e:
            print(f"创建数据表时出现错误：{e}")

    def __user_insert(self, tb_name):
        """
        Inserts data into the MySQL table.

        Args:
            tb_name (str): The name of the table.
        """
        try:
            insert_query = f"""
            INSERT INTO {tb_name} (账号url, 账号ID, 账号昵称, 性别, 关系状况, 个人描述)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            # 执行多条插入，每个元素是一个字典
            for post in self.data_list:
                self.cursor.execute(insert_query, (
                    post['账号url'], post['账号ID'], post['账号昵称'],
                    post['性别'], post['关系状况'], post['个人描述']
                ))

            self.db.commit()
            print('-数据插入成功-')

        except pymysql.MySQLError as e:
            print(f"执行插入操作时出现错误：{e}")
            self.db.rollback()

    def store_friends_following_followers_mode_mysql(self, db_name, tb_name):
        """
        Stores data into a MySQL database.

        Args:
            db_name (str): The name of the database.
            tb_name (str): The name of the table.
        """
        try:
            # 连接数据库
            self.db = pymysql.connect(host='localhost', user='root', passwd='wz131', port=3306)
            self.cursor = self.db.cursor()
            print('-连接成功-')

            # 检查并创建数据库（如果不存在）
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            print('-数据库已检查-')

            # 选择数据库
            self.cursor.execute(f"USE {db_name}")

            # 创建数据表
            self.__create_friends_following_followers_table(tb_name)

            # 插入数据
            self.__friends_following_followers_insert(tb_name)
            # print('-正在插入数据-')

            # 关闭mysql
            self.db.close()
            print('-连接关闭-')

        except pymysql.MySQLError as e:
            print(f"连接数据库时出现错误：{e}")

    def __create_friends_following_followers_table(self, tb_name):
        """
        Creates a table in the MySQL database if it doesn't exist.

        Args:
            tb_name (str): The name of the table.
        """
        try:
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {tb_name} (
                MAIN_ID INT AUTO_INCREMENT PRIMARY KEY,
                own_url Text,
                name Text,
                profile_url Text,
                profile_image_url Text,
                descs Text,
                cursors Text
            );
            """
            self.cursor.execute(create_table_query)
            print('-表已检查-')

        except pymysql.MySQLError as e:
            print(f"创建数据表时出现错误：{e}")

    def __friends_following_followers_insert(self, tb_name):
        """
        Inserts data into the MySQL table.

        Args:
            tb_name (str): The name of the table.
        """
        try:
            insert_query = f"""
            INSERT INTO {tb_name} (own_url, name, profile_url, profile_image_url, descs, cursors)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            # 执行多条插入，每个元素是一个字典
            for post in self.data_list:
                self.cursor.execute(insert_query, (
                    post['own_url'], post['name'], post['profile_url'],
                    post['profile_image_url'], post['desc'], post['cursor']
                ))

            self.db.commit()
            print('-数据插入成功-')

        except pymysql.MySQLError as e:
            print(f"执行插入操作时出现错误：{e}")
            self.db.rollback()

    def store_post_mode_mysql(self, db_name, tb_name):
        """
        Stores data into a MySQL database.

        Args:
            db_name (str): The name of the database.
            tb_name (str): The name of the table.
        """
        try:
            # 连接数据库
            self.db = pymysql.connect(host='localhost', user='root', passwd='wz131', port=3306)
            self.cursor = self.db.cursor()
            print('-连接成功-')

            # 检查并创建数据库（如果不存在）
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            print('-数据库已检查-')

            # 选择数据库
            self.cursor.execute(f"USE {db_name}")

            # 创建数据表
            self.__create_post_table(tb_name)

            # 插入数据
            self.__post_insert(tb_name)
            # print('-正在插入数据-')

            # 关闭mysql
            self.db.close()
            print('-连接关闭-')

        except pymysql.MySQLError as e:
            print(f"连接数据库时出现错误：{e}")

    def __create_post_table(self, tb_name):
        """
        Creates a table in the MySQL database if it doesn't exist.

        Args:
            tb_name (str): The name of the table.
        """
        try:
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {tb_name} (
                MAIN_ID INT AUTO_INCREMENT PRIMARY KEY,
                external_id Text,
                post_id Text,
                post_url Text,
                text Text,
                creater_id Text,
                creater_name Text,
                creater_url Text,
                creation_time Text,
                comments_count int,
                reaction_count Text
            );
            """
            self.cursor.execute(create_table_query)
            print('-表已检查-')

        except pymysql.MySQLError as e:
            print(f"创建数据表时出现错误：{e}")

    def __post_insert(self, tb_name):
        """
        Inserts data into the MySQL table.

        Args:
            tb_name (str): The name of the table.
        """
        try:
            insert_query = f"""
            INSERT INTO {tb_name} (external_id, post_id, post_url, text, creater_id, creater_name,creater_url,creation_time,comments_count,reaction_count)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            # 执行多条插入，每个元素是一个字典
            for post in self.data_list:
                self.cursor.execute(insert_query, (
                    post['X_id'], post['post_id'], post['post_url'],
                    post['text'], post['creater_id'], post['creater_name'],
                    post['creater_url'],post['creation_time'],post['comments_count'],post['reaction_count']
                ))

            self.db.commit()
            print('-数据插入成功-')

        except pymysql.MySQLError as e:
            print(f"执行插入操作时出现错误：{e}")
            self.db.rollback()


