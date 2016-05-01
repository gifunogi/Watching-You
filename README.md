# Watching-You
消された過去を掘り返す。


自分のタイムライン上でTweetが消されたとき，それを通知してデータベースファイルに保存するプログラムです．pythonのTwitter APIモジュールである[tweepy](https://github.com/tweepy/tweepy)を使用しています．

```
CK = ""
CS = ""
AT = ""
AS = ""
```
に，それぞれ[Twitter Developers](https://dev.twitter.com/)で取得したConsumer Key，Consumer Key Secret，Access Token，Access Token Secretを入力し，`python watchingYou.py`のコマンドからプログラムの起動が可能です．
プログラムの起動後から，自身のタイムラインのツイート情報を`tweet.db`ファイルに保存します．もしも，タイムライン上でツイートの削除が行えわれ，かつ`tweet.db`ファイル内に該当データがあった場合，
`--****(@****)さんが以下のツイートをツイ消ししました．--`
と表示し，そのデータを`deleted.db`ファイルにコピーします．
