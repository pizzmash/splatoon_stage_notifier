import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MQTT_HOST = os.environ.get("MQTT_HOST")
MQTT_PORT = int(os.environ.get("MQTT_PORT"))
MQTT_CERTS = os.environ.get("MQTT_CERTS")
CHANNEL_TOKEN = os.environ.get("CHANNEL_TOKEN")
CHANNEL_TOPIC = os.environ.get("CHANNEL_TOPIC")
IKSM_SESSION = os.environ.get("IKSM_SESSION")
GA_NAME = os.environ.get("GA_NAME")
