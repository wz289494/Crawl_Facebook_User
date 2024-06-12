import re
import json
import datetime

class Extract(object):
    def user_extract(self, user_page, url):
        """
        Extract user information from the user page content.

        Parameters:
        user_page (str): HTML content of the user page.
        url (str): URL of the user page.

        Returns:
        dict: Extracted user information.
        """
        user_dic = {}

        # URL information
        user_dic['account_url'] = url

        # Basic profile information
        user_id_match = re.search('"userID":"(.*?)"', user_page, re.S)
        user_dic['account_id'] = user_id_match.group(1) if user_id_match else ''

        nickname_match = re.search('"data":{"name":"(.*?)"', user_page, re.S)
        user_dic['account_nickname'] = nickname_match.group(1) if nickname_match else ''

        gender_match = re.search('"gender":"(.*?)"', user_page, re.S)
        user_dic['gender'] = gender_match.group(1) if gender_match else ''

        # Extract personal information from the top of the page
        pattern = re.compile(r'{"__bbox":{"complete":false,"result":{"data":{"user":{"profile_header_renderer".*?</script>', re.DOTALL)
        match = pattern.search(user_page)
        lit_page = match.group(0)

        rela_str = ''
        relas = list(set(re.findall(r'"color_ranges":\[\],"text":"(.*?)"', lit_page, re.S)))
        for rela in relas:
            rela_str += bytes(rela, 'utf-8').decode('unicode_escape') + '\n'

        # Extract relationship status
        user_dic['relationship_status'] = self.__clean_unicode(rela_str)

        # Extract personal information from the bottom of the page
        pattern = re.compile(r'"__bbox":\{"complete":true,"result":\{"data":\{"user".*?</script>', re.DOTALL)
        match = pattern.search(user_page)
        lit_page = match.group(0)

        desc_str = ''
        descs = list(set(re.findall(r'"color_ranges":\[\],"text":"(.*?)"', lit_page, re.S)))
        for desc in descs:
            desc_str += bytes(desc, 'utf-8').decode('unicode_escape') + '\n'

        # Extract personal description
        user_dic['personal_description'] = self.__clean_unicode(desc_str)

        return user_dic

    def __clean_unicode(self, text):
        """
        Clean the Unicode text.

        Parameters:
        text (str): Text to be cleaned.

        Returns:
        str: Cleaned text.
        """
        cleaned_text = ''
        for char in text:
            try:
                char.encode('utf-8').decode('utf-8')
                cleaned_text += char
            except UnicodeEncodeError:
                cleaned_text += '\ufffd'
        return cleaned_text

    def friends_following_followers_extract(self, following_json, url):
        """
        Extract friends/following/followers information from the JSON response.

        Parameters:
        following_json (str): JSON response containing the information.
        url (str): URL of the user page.

        Returns:
        tuple: End cursor, has_more flag, and list of user information.
        """
        data = json.loads(following_json)

        end_cursor = data["data"]["node"]["pageItems"]["page_info"]['end_cursor']
        has_more = data["data"]["node"]["pageItems"]["page_info"]['has_next_page']

        user_info = []
        for edge in data["data"]["node"]["pageItems"]["edges"]:
            user = {
                'own_url': url,
                "id": edge["node"]["id"],
                "name": edge["node"]["title"]["text"],
                "profile_url": edge["node"]["url"],
                "profile_image_url": edge["node"]["image"]["uri"],
                "desc": edge["node"]["subtitle_text"]["text"] if "subtitle_text" in edge["node"] else "",
                "cursor": edge["cursor"]
            }
            user_info.append(user)

        return end_cursor, has_more, user_info

    def post_extract(self, json_data):
        """
        Extract post information from the JSON response.

        Parameters:
        json_data (str): JSON response containing the post information.

        Returns:
        tuple: Extracted post data, has_more flag, and cursor.
        """
        json_data = json.loads(json_data)

        data = {}

        # Extract cursor
        edge = json_data.get('data', {}).get('node', {}).get('timeline_list_feed_units', {}).get('edges', [])[0]

        # Locate the node
        node = edge.get('node', {})

        # Extract X_id and post_id
        data['X_id'] = node.get('id', None)
        data['post_id'] = node.get('post_id', None)

        # Locate the story
        content_story = node.get('comet_sections', {}).get('content', {}).get('story', {})

        # Extract post URL
        data['post_url'] = content_story.get('wwwURL', None)

        # Extract text content
        message = content_story.get('message', None)
        data['text'] = message.get('text', None) if message else None

        # Extract creator information
        creater = content_story.get('actors', [{}])[0]
        data['creator_id'] = creater.get('id', None)
        data['creator_name'] = creater.get('name', None)
        data['creator_url'] = creater.get('url', None)

        # Extract creation time
        metadata = node.get('comet_sections', {}).get('context_layout', {}).get('story', {}).get('comet_sections', {}).get('metadata', [])
        if metadata:
            creation_time = metadata[0].get('story', {}).get('creation_time', None)
            data['creation_time'] = self.__convert_time(creation_time)
        else:
            data['creation_time'] = None

        # Extract comments and interaction count
        feedback = node.get('comet_sections', {}).get('feedback', {}).get('story', {}).get('comet_feed_ufi_container', {}).get('story', {}).get('feedback_context', {}).get('feedback_target_with_context', {}).get('ufi_renderer', {}).get('feedback', {})
        data['comments_count'] = feedback.get('comment_rendering_instance', {}).get('comments', {}).get('total_count', None)
        data['reaction_count'] = feedback.get('comet_ufi_summary_and_actions_renderer', {}).get('feedback', {}).get('i18n_reaction_count', None)

        # Set has_more flag
        has_more = edge is not None

        # Extract cursor
        cursor = edge.get('cursor', None)

        return data, has_more, cursor

    def __convert_time(self, timestamp):
        """
        Convert a timestamp to a formatted datetime string.

        Parameters:
        timestamp (int): Timestamp to be converted.

        Returns:
        str: Formatted datetime string.
        """
        # Convert timestamp to datetime object
        dt = datetime.datetime.fromtimestamp(timestamp)

        # Format datetime object as string
        return dt.strftime("%Y-%m-%d %H:%M:%S")
