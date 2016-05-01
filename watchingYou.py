# -*- coding: utf-8 -*-
import re
import json
import sqlite3
from tweepy.streaming import StreamListener, Stream
from tweepy.auth import OAuthHandler
from tweepy.api import API

# データベースのパス
TWEET_PATH = "tweet.db"
DELETED_PATH = "deleted.db"

# 認証情報
CK = ""
CS = ""
AT = ""
AS = ""

def get_oauth():
	auth = OAuthHandler(CK, CS)
	auth.set_access_token(AT, AS)
	return auth

class MyStreamListener(StreamListener):
	def on_data(self, data):
		stream = json.loads(data)
		if 'delete' in stream:
			user_id = stream['delete']['status']['user_id']
			tweet_id = stream['delete']['status']['id']
			screen = api.get_user(user_id).screen_name
			cur = tweet_DB.execute("SELECT * FROM sqlite_master WHERE type='table' and name='{screen}'".format(screen=screen))
			if not cur.fetchone() is None:
				deleted = tweet_DB.execute("SELECT * FROM '{screen}' where tweet_id = '{tweet_id}'".format(screen=screen, tweet_id=tweet_id)).fetchone()
				if not isinstance(deleted, type(None)):
					name = api.get_user(user_id).name
					tweet = deleted[1]
					print(u"--{name}(@{screen})さんが以下のツイートをツイ消ししました．--".format(name=name, screen=screen))
					print(u"{tweet}\n".format(tweet=tweet))
					try: deleted_DB.execute("CREATE TABLE '{screen}'(tweet_id, tweet, created_at)".format(screen=screen))
					except: pass
					# try: deleted_DB.execute("INSERT INTO '{screen}'VALUES{deleted}".format(screen=screen, deleted=deleted))
					# except: pass
					deleted_DB.execute("INSERT INTO '{screen}'VALUES{deleted}".format(screen=screen, deleted=deleted))
					deleted_DB.commit()
			
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
			try: tweet_DB.execute("CREATE TABLE '{screen}'(tweet_id, tweet, created_at)".format(screen=screen))
			except: pass
			try: tweet_DB.execute("INSERT INTO '{screen}'VALUES('{tweet_id}', '{tweet}', '{created_at}')".format(screen=screen, tweet_id=tweet_id, tweet=tweet, created_at=created_at))
			except: pass
			tweet_DB.commit()

if __name__ == '__main__':
	auth = get_oauth()
	api = API(auth_handler=auth, retry_count=1)
	tweet_DB = sqlite3.connect(TWEET_PATH)
	deleted_DB = sqlite3.connect(DELETED_PATH)
	stream = Stream(auth, MyStreamListener(), secure=True)
	stream.userstream()
	