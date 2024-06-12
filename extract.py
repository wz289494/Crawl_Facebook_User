import re
import json
import datetime

class Extract(object):
    def user_extract(self,user_page,url):
        user_dic = {}

        # url信息
        user_dic['账号url'] = url

        # 页面基础资料
        user_id_match = re.search('"userID":"(.*?)"', user_page, re.S)
        user_dic['账号ID'] = user_id_match.group(1) if user_id_match else ''

        nickname_match = re.search('"data":{"name":"(.*?)"', user_page, re.S)
        user_dic['账号昵称'] = nickname_match.group(1) if nickname_match else ''

        gender_match = re.search('"gender":"(.*?)"', user_page, re.S)
        user_dic['性别'] = gender_match.group(1) if gender_match else ''

        # 页面上方个人资料，text可以定位的
        pattern = re.compile(r'{"__bbox":{"complete":false,"result":{"data":{"user":{"profile_header_renderer".*?</script>', re.DOTALL)
        match = pattern.search(user_page)
        lit_page = match.group(0)

        rela_str = ''
        relas = list(set(re.findall(r'"color_ranges":\[\],"text":"(.*?)"', lit_page, re.S)))
        for rela in relas:
            rela_str += bytes(rela, 'utf-8').decode('unicode_escape') + '\n'

        # 获取页面下方个人资料
        user_dic['关系状况'] = self.__clean_unicode(rela_str)

        # 页面下方个人资料，text可以定位的
        pattern = re.compile(r'"__bbox":\{"complete":true,"result":\{"data":\{"user".*?</script>', re.DOTALL)
        match = pattern.search(user_page)
        lit_page = match.group(0)

        desc_str = ''
        descs = list(set(re.findall(r'"color_ranges":\[\],"text":"(.*?)"', lit_page, re.S)))
        for desc in descs:
            desc_str += bytes(desc, 'utf-8').decode('unicode_escape') + '\n'

        # 获取页面下方个人资料
        user_dic['个人描述'] = self.__clean_unicode(desc_str)

        return user_dic

    def __clean_unicode(self,text):
        cleaned_text = ''
        for char in text:
            try:
                char.encode('utf-8').decode('utf-8')
                cleaned_text += char
            except UnicodeEncodeError:
                cleaned_text += '\ufffd'
        return cleaned_text

    def friends_following_followers_extract(self,following_json,url):
        data = json.loads(following_json)

        end_cursor = data["data"]["node"]["pageItems"]["page_info"]['end_cursor']
        has_more = data["data"]["node"]["pageItems"]["page_info"]['has_next_page']

        user_info = []
        for edge in data["data"]["node"]["pageItems"]["edges"]:
            user = {
                'own_url' : url,
                "id": edge["node"]["id"],
                "name": edge["node"]["title"]["text"],
                "profile_url": edge["node"]["url"],
                "profile_image_url": edge["node"]["image"]["uri"],
                "desc": edge["node"]["subtitle_text"]["text"] if "subtitle_text" in edge["node"] else "",
                "cursor": edge["cursor"]
            }
            user_info.append(user)

        return end_cursor , has_more , user_info

    def post_extract(self,json_data):
        json_data = json.loads(json_data)

        data = {}

        # 提取cursor
        edge = json_data.get('data', {}).get('node', {}).get('timeline_list_feed_units', {}).get('edges', [])[0]

        # 定位到node
        node = edge.get('node', {})

        # 提取Xid和post_id
        data['X_id'] = node.get('id', None)
        data['post_id'] = node.get('post_id', None)

        # 定位到story
        content_story = node.get('comet_sections', {}).get('content', {}).get('story', {})

        # 提取wwwURL
        data['post_url'] = content_story.get('wwwURL', None)

        # 提取文本内容
        message = content_story.get('message', None)
        if message != None:
            data['text'] = message.get('text', None)
        else:
            data['text'] = None

        # 提取发布者信息
        creater = content_story.get('actors', [{}])[0]
        data['creater_id'] = creater.get('id', None)
        data['creater_name'] = creater.get('name', None)
        data['creater_url'] = creater.get('url', None)

        # 提取创建时间
        metadata = node.get('comet_sections', {}).get('context_layout', {}).get('story', {}).get('comet_sections',{}).get('metadata',[])
        if metadata:
            creation_time = metadata[0].get('story', {}).get('creation_time', None)
            data['creation_time'] = self.__convert_time(creation_time)
        else:
            data['creation_time'] = None

        # 提取评论和互动总数
        feedback = node.get('comet_sections', {}).get('feedback', {}).get('story', {}).get('comet_feed_ufi_container', {}).get('story', {}).get('feedback_context', {}).get('feedback_target_with_context', {}).get('ufi_renderer', {}).get('feedback', {})
        data['comments_count'] = feedback.get('comment_rendering_instance', {}).get('comments', {}).get('total_count', None)
        data['reaction_count'] = feedback.get('comet_ufi_summary_and_actions_renderer', {}).get('feedback',{}).get('i18n_reaction_count', None)

        # 设置参数
        if edge !=None:
            has_more = True
        else:
            has_more = False

        # 提取cursor
        cursor = edge.get('cursor', None)

        return data,has_more,cursor

    def __convert_time(self,timestamp):
        # 将时间戳转换为datetime对象
        dt = datetime.datetime.fromtimestamp(timestamp)

        # 格式化datetime对象为字符串
        return dt.strftime("%Y-%m-%d %H:%M:%S")