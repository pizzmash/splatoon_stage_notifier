# SplatoonStageNotifier
GoogleHomeにスプラのステージ情報を喋らせた〜い

## About
GoogleHome-IFTTT-Beebotte-Server-GoogleHomeで質問に答えさせる。iksm_sessionは別途必要。そのうちIFTTT使わんでもできるようにできればいいね。

## Preparation

### Beebotteの準備
チャンネルとトピック作る。

### IFTTの準備
GoogleAssistantとWebhookで喋り掛けられたらBeebotteで作ったチャンネルにデータを投げる。後述の6種類のJSONをうまい具合にBeebotteに投げるように設定してください。私はあほなのでAppletを6つ作った。

#### Webhook
各項目を以下のように設定

| 項目 | 内容 |
| - | - |
| URL | https\://api.beebotte.com/v1/data/publish/`CHANNEL_NAME`/`TOPIC`?token=`CHANNEL_TOKEN` |
| Method | POST |
| Content | application/json |
| Body | うまい具合に下のどれかになるようにする。<br> {"data": {"cmd": "current"}} <br> {"data": {"cmd": "next"}} <br> {"data": {"cmd": "search", "rule": "area"}} <br> {"data": {"cmd": "search", "rule": "yagura"}} <br> {"data": {"cmd": "search", "rule": "hoko"}} <br> {"data": {"cmd": "search", "rule": "asari"}} |

### Serverの準備

#### required
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [Paho MQTT](https://github.com/eclipse/paho.mqtt.python)
- [pychromecast](https://github.com/home-assistant-libs/pychromecast)

以下でインストール
```
$ pip install -r requirements.txt
```

#### Beebotteの証明書のダウンロード
```
$ wget https://beebotte.com/certs/mqtt.beebotte.com.pem
```

#### トークンの設定
`.env`を作って`.env.sample`を参考にトークンとかを設定する

| 変数 | 中身 |
| - | - |
| MQTT_HOST | mqtt.beebotte.com |
| MQTT_PORT | 8883 |
| MQTT_CERTS | 証明書のパス |
| CHANNEL_TOKEN | チャンネルのトークン |
| CHANNEL_TOPIC | `CHANNEL_NAME`/`TOPIC` |
| IKSM_SESSION | iksm_session |
| GA_NAME | GoogleHomeの名前<br>"リビングルーム"とか |

#### 実行
```
$ python main.py
on_connect: rc: 0 # Beebotteに繋がった
on_message: data: {'cmd': 'current'} # メッセージを受信した時
```
systemdとかに登録した方が現実的


## Usage
IFTTTのGoogleAssistantでどう設定したかにもよるけど、
```
> Hey, Google、ルール教えて
現在のガチマッチのルールはガチヤグラ、ステージはアジフライスタジアムと海女美術大学です。

> Hey, Google、次のルール教えて
21時からのガチマッチのルールはガチアサリ、ステージはアンチョビットゲームズとエンガワ河川敷です。

> Hey, Google、次のエリア教えて
次のガチエリアは1時から、ステージはムツゴ楼とザトウマーケットです。
```
