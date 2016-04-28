# -*- coding: utf-8 -*-
import re
import json
import sqlite3
from tweepy.streaming import StreamListener, Stream
from tweepy.auth import OAuthHandler
from tweepy.api import API
from datetime import timedelta

# データベースのパス
DB_PATH = "tweet.db"

# 認証情報
CK = ""
CS = ""
AT = ""
AS = ""

def get_oauth():
	auth = OAuthHandler(CK, CS)
	auth.set_access_token(AT, AS)
	return auth

class CustomStreamListener(StreamListener):
	def on_data(self, data):
		stream = json.loads(data)
		if 'delete' in stream:
			user_id = stream['delete']['status']['user_id']
			tweet_id = stream['delete']['status']['id']
			if not isinstance(con.execute("SELECT * FROM '{user_id}' where tweet_id = '{tweet_id}'".format(user_id=user_id, tweet_id=tweet_id)).fetchone(), type(None)):
				name = api.get_user(user_id).name
				screen = api.get_user(user_id).screen_name
				tweet = con.execute("SELECT * FROM '{user_id}' where tweet_id = '{tweet_id}'".format(user_id=user_id, tweet_id=tweet_id)).fetchone()[1]
				print(u"""--{name}(@{screen})さんが次のツイートをツイ消ししました。--""".format(name=name, screen=screen))
				print(u"{tweet}\n".format(tweet=tweet))
			
		elif 'text' in stream:
			tweet = stream['text'].replace("'", '"')
			name = stream['user']['name']
			screen = stream['user']['screen_name']
			user_id = stream['user']['id']
			created_at = stream['created_at']
			tweet_id = stream['id']
			print(u"{tweet}".format(tweet=tweet))
			print(u"{name}(@{screen}) {created_at}".format(name=name, screen=screen, created_at=created_at))
			print(u"TweetID: {tweet_id}\n".format(tweet_id=tweet_id))
			try: con.execute("CREATE TABLE '{user_id}'(tweet_id, tweet)".format(user_id=user_id))
			except: pass
			try: con.execute("INSERT INTO '{user_id}'VALUES('{tweet_id}', '{tweet}')".format(user_id=user_id, tweet_id=tweet_id, tweet=tweet))
			except: pass
			con.commit()

if __name__ == '__main__':
	auth = get_oauth()
	api = API(auth_handler=auth, retry_count=1)
	con = sqlite3.connect(DB_PATH)
	stream = Stream(auth, CustomStreamListener(), secure=True)
	stream.userstream()
	


