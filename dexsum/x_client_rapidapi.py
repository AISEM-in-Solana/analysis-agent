import http.client
import json


class TwitterApiClient:
    
    def __init__(self, api_key, host):
        self.conn = http.client.HTTPSConnection("twitter241.p.rapidapi.com")
        self.headers = {
                    'x-rapidapi-key': api_key,
                    'x-rapidapi-host': host
                }
    
    def parse_response(self, res):
        data = res.read()
        data = json.loads(data)
        return data
    
    def get_user_by_username(self, username):
        """Fetch the user information including rest_id using username."""
        self.conn.request("GET", f"/user?username={username}", headers=self.headers)

        res = self.conn.getresponse()
        data = self.parse_response(res)
        try:
            uid = data['result']['data']['user']['result']["rest_id"]
            return uid
        except:
            return None
        
    def get_posts_by_rest_id(self, rest_id, num_posts = 10):
        """Fetch posts by rest_id."""
        self.conn.request("GET", f"/user-tweets?user={rest_id}&count={num_posts}", headers=self.headers)
        res = self.conn.getresponse()
        data = self.parse_response(res)
        instructions = data['result']['timeline']['instructions']
        post_ids = []
        for instrucion in instructions:
            entries = instrucion.get("entries", None)
            if entries:
                for entry in entries:
                    tmp = entry['content'].get('itemContent', {}).get('tweet_results', {}).get('result', {}).get('rest_id', '')
                    if tmp: post_ids.append(tmp)
        return list(dict.fromkeys(post_ids).keys())
    
    def get_post_content(self, post_id):
        """Fetch detail tweet by post_id."""
        self.conn.request("GET", f"/tweet?pid={post_id}", headers=self.headers)
        res = self.conn.getresponse()
        data = self.parse_response(res)
        return data.get("tweet", {}).get("full_text", "")
    
