#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import time
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
                    print("--{name}(@{screen})さんが以下のツイートを消しました．--".format(name=name, screen=screen))
                    print("\033[36m" + "{tweet}\n".format(tweet=tweet) + "\033[39m")
                    try:
                        deleted_DB.execute("CREATE TABLE '{screen}'(tweet_id, tweet, created_at)".format(screen=screen))
                    except:
                        pass
                    deleted_DB.execute("INSERT INTO '{screen}'VALUES{deleted}".format(screen=screen, deleted=deleted))
                    deleted_DB.commit()
            
        elif 'text' in stream:
            tweet = stream['text'].replace("'", '"')
            name = stream['user']['name']
            screen = stream['user']['screen_name']
            user_id = stream['user']['id']
            created_at = stream['created_at']
            tweet_id = stream['id']
            print("\033[36m" + "{tweet}".format(tweet=tweet) + "\033[39m")
            print("{name}(@{screen}) {created_at}".format(name=name, screen=screen, created_at=created_at))
            print("TweetID: {tweet_id}\n".format(tweet_id=tweet_id))
            try:
                tweet_DB.execute("CREATE TABLE '{screen}'(tweet_id, tweet, created_at)".format(screen=screen))
            except:
                pass
            try:
                tweet_DB.execute("INSERT INTO '{screen}'VALUES('{tweet_id}', '{tweet}', '{created_at}')".format(screen=screen, tweet_id=tweet_id, tweet=tweet, created_at=created_at))
            except:
                pass
            tweet_DB.commit()

def get_oauth():
    auth = OAuthHandler(CK, CS)
    auth.set_access_token(AT, AS)
    return auth

if __name__ == '__main__':
    auth = get_oauth()
    api = API(auth_handler=auth, retry_count=1)
    tweet_DB = sqlite3.connect(TWEET_PATH)
    deleted_DB = sqlite3.connect(DELETED_PATH)
    stream = Stream(auth, MyStreamListener(), secure=True)
    while True:
        try:
            stream.userstream()
        except:
            print("\033[31m" + "ConnectionError!")
            print("Reconnect after 10 seconds." + "\033[39m")
            for i in range(11):
                print(".", end="")
                sys.stdout.flush()
                time.sleep(1)
            print()
