from tweepy import Client
import tweepy

class XClient():
    def __init__(self,
                bearer_token, 
                consumer_key, 
                consumer_secret, 
                access_token, 
                access_token_secret,
                wait_on_rate_limit  = False
            ):
        
        self.client = Client(
            bearer_token, 
            consumer_key, 
            consumer_secret, 
            access_token, 
            access_token_secret,
            wait_on_rate_limit = wait_on_rate_limit
            )
        
        auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
        self.api_v1 = tweepy.API(auth)

    # Function to fetch replies to a specific tweet
    def fetch_replies(self, client, tweet_id):
        try:
            query = f"conversation_id:{tweet_id}"
            response = client.search_recent_tweets(
                query=query, 
                max_results=10, 
                tweet_fields=["id", "text", "author_id", "created_at"], 
                user_auth = True
            )
            return response.data if response else []
        except Exception as e:
            print(f"Error fetching replies: {e}")
            return []

    # Function to reply to the latest comment
    def reply_to_latest_comment(self, tweet_id, reply_text):
        try:
            # Fetch replies to the tweet
            replies = self.fetch_replies(self.client, tweet_id)
            
            if not replies:
                print("No replies found.")
                return
            
            # Find the latest reply (most recent creation time)
            latest_reply = sorted(replies, key=lambda x: x.created_at, reverse=True)[0]
            
            # Post a reply to the latest comment
            self.client.create_tweet(
                text=f"@{latest_reply.author_id} {reply_text}",
                in_reply_to_tweet_id=latest_reply.id,
                user_auth = True
            )
            print(f"Replied to tweet ID {latest_reply.id}: {reply_text}")
        
        except Exception as e:
            print(f"Error replying to the latest comment: {e}")

    def get_latest_tweet(self, username, number_tweets: int = 5):
        """
        Fetch the latest tweet from a given username.

        Args:
            client: Tweepy Client object.
            username: The Twitter username to fetch the latest tweet for.

        Returns:
            Dictionary containing the latest tweet's ID, text, and creation date.
        """
        try:
            user = self.client.get_user(username=username)
            user_id = user.data.id

            # Fetch the latest tweet
            tweets = self.client.get_users_tweets(
                id=user_id, 
                max_results=number_tweets,  # Get only the latest tweet
                tweet_fields=["created_at"]
            )

            if tweets.data:
                return {
                    "ids": [x.id for x in tweets.data],
                    "texts": [x.text for x in tweets.data],
                    "created_ats": [x.created_at for x in tweets.data]
                }
            else:
                print(f"No tweets found for user @{username}.")
                return None
        except Exception as e:
            print(f"Error fetching the latest tweet: {e}")
            return None

    def reply_to_tweet(self, tweet_id, reply_text):
        try:
            # Reply to the given tweet ID
            response = self.client.create_tweet(
                text=reply_text,
                in_reply_to_tweet_id=tweet_id
            )
            print(f"Reply posted successfully: {response.data}")
        except Exception as e:
            print(f"Error replying to tweet: {e}")

    def upload_image(self, image_path: str):
        media = self.api_v1.media_upload(image_path)
        return media.media_id
    
    def post(self, content: str, user_auth: bool = True, media_ids: list = None):
        self.client.create_tweet(text = content, user_auth = user_auth, media_ids=media_ids)
        
if __name__ == "__main__":

    # Your tweet ID and username
    # my_tweet_id = "1867240952030691410"  # Replace with your tweet ID
    my_username = "@madokaai_sol"  # Replace with your Twitter handle

    from telethon import TelegramClient, events
    import re
    import os
    from dotenv import load_dotenv
    from x_client import XClient

    load_dotenv()

    # Your API credentials
    API_ID = '21451416'
    API_HASH = 'c4eecd06ec1f1dfbae429a397b182bd3'
    CHANNEL_USERNAME = '@TrendingOnDS'  # e.g., 'examplechannel'

    # Create a client instance
    client = TelegramClient('session_name', API_ID, API_HASH)
    API_KEY = os.environ['API_KEY']
    API_SECRET_KEY = os.environ['API_SECRET_KEY']
    ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
    BEARER_TOKEN = os.environ["BEARER_TOKEN"]
    CLIENT_ID = os.environ["CLIENT_ID"]
    CLIENT_SECRET = os.environ["CLIENT_SECRET"]

    OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
    TELE_TOKEN = os.environ['TELE_TOKEN']
    TELE_GROUP_ID = os.environ['TELE_GROUP_ID']


    x_client = XClient(
        bearer_token= BEARER_TOKEN,
        consumer_key= API_KEY,
        consumer_secret= API_SECRET_KEY,
        access_token= ACCESS_TOKEN,
        access_token_secret= ACCESS_TOKEN_SECRET,
        wait_on_rate_limit = True
    )
    
    data = x_client.get_latest_tweet("ChillAmigoSol_",5 )
    print(data)