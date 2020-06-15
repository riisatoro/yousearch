from django.apps import AppConfig
from googleapiclient.discovery import build
import api_token


class MainConfig(AppConfig):
    name = 'main'
