import sys
import time
import requests
import json
import urllib.parse

import settings
import paho.mqtt.client as mqtt
import pychromecast

import textbuilder


MQTT_HOST = settings.MQTT_HOST
MQTT_PORT = settings.MQTT_PORT
MQTT_CERTS = settings.MQTT_CERTS
CHANNEL_TOKEN = settings.CHANNEL_TOKEN
CHANNEL_TOPIC = settings.CHANNEL_TOPIC
IKSM_SEISSION = settings.IKSM_SESSION
GA_NAME = settings.GA_NAME


def requests_schedules():
    url = "https://app.splatoon2.nintendo.net/api/schedules"
    headers = {"Cookie": f"iksm_session={IKSM_SEISSION}"}
    schedules = requests.get(url, headers=headers).json()
    return schedules


def make_schedule_text_from_json(schedules, cmds):
    if cmds["cmd"] == "current":
        tb = textbuilder.CurrentRuleTB(schedules)
    elif cmds["cmd"] == "next":
        tb = textbuilder.NextRuleTB(schedules)
    elif cmds["cmd"] == "search":
        tb = textbuilder.SearchedRuleTB(schedules)
    return tb.build(**cmds)


def get_chromecast():
    casts, _ = pychromecast.get_listed_chromecasts(friendly_names=[GA_NAME])
    if len(casts) == 0:
        print("${GA_NAME} not founds")
        return None
    else:
        return casts[0]


def notify(cast, text):
    t_quote = urllib.parse.quote(text)
    url = "http://translate.google.com/translate_tts?ie=UTF-8&q=" + t_quote + "&tl=ja&client=tw-ob"
    if not cast.is_idle:
        print("Killing current running app")
        cast.quit_app()
        time.sleep(5)
    cast.wait()
    cast.media_controller.play_media(url, "audio/mp3")
    cast.media_controller.block_until_active()


def on_connect(mqttc, obj, flags, rc):
    print("on_connect: rc: " + str(rc))


def on_message(mqttc, obj, msg):
    data = json.loads(msg.payload.decode("utf-8"))["data"]
    print("on_message: data:", data)

    cast = get_chromecast()
    schedules = requests_schedules()
    text = make_schedule_text_from_json(schedules, data)
    notify(cast, text)


def main():
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.username_pw_set(CHANNEL_TOKEN)
    client.tls_set(MQTT_CERTS)
    client.connect(MQTT_HOST, MQTT_PORT)
    client.subscribe(CHANNEL_TOPIC)
    client.loop_forever()


if __name__ == "__main__":
    main()
