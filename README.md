# Watching-You
お前を見ているぞ．

自分のタイムライン上でツイートが消されたとき，それを通知してデータベースファイルに保存するプログラムです．PythonのTwitter APIモジュールである[tweepy](https://github.com/tweepy/tweepy)を使用しています．

```
CK = ""
CS = ""
AT = ""
AS = ""
```
以上に，それぞれ[Twitter Developers](https://dev.twitter.com/)で取得したConsumer Key，Consumer Key Secret，Access Token，Access Token Secretを入力し，
```
python watchingYou.py
```
のコマンドからプログラムの起動が可能です．
プログラムの起動後から，自身のタイムラインのツイート情報を`tweet.db`ファイルに保存します．また，ターミナル上ではタイムラインにツイートを取得した際に，
```
[ツイート文字列]
****(@****) [Week] [Month] DD HH:MM:SS +0000 YYYY
TweetID: ******************
```
と言った書式で出力を行います．

もしも，タイムライン上でツイートの削除が行えわれ，かつ`tweet.db`ファイル内に該当データがあった場合，
```
--****(@****)さんが以下のツイートを消しました．--．--
```
と表示し，そのツイートデータを`deleted.db`ファイルにコピーします．

UserStreamの接続にした場合は，
```
ConnectionError!
Reconnect after 10 seconds.
```
と表示し，10秒後に再接続を行います．

プログラムの終了には`Ctrl + c`，もしくはターミナルの終了から行って下さい．
