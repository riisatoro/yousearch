from django.shortcuts import render
from django.views.generic import TemplateView

from googleapiclient.discovery import build
import api_token

import random
import json
import os


#youtube api requests
def get_test(youtube, query):
    request = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=13
    )
    response = request.execute()
    data = []
    for item in response["items"]:
        tmp = {
            "name": item["snippet"]["title"],
            "link": "https://www.youtube.com/watch?v="+item["id"]["videoId"],
            "iframe": "https://www.youtube.com/embed/"+item["etag"],
            "date": item["snippet"]["publishedAt"].split("T")[0],
            "preview": item["snippet"]["thumbnails"]["medium"]["url"],
            "liked": random.choice([True, False])
        }
        data.append(tmp)
    return data


class Search(TemplateView):
    template_name = "search.html"
    youtube = build('youtube', 'v3', developerKey=api_token.token)

    def get(self, request):
        args = {}
        return render(request, self.template_name, args)

    def post(self, request):
        query = request.POST["search"]
        video = get_test(self.youtube, query)
        '''
        module_dir = os.path.dirname(__file__)
        path = os.path.join(module_dir, "data.json")
        with open(path, 'r') as file:
            video = json.load(file)
        '''
        args = {
            "query": query,
            "main_video": video[0],
            "other_video": video[1:]
            }

        return render(request, self.template_name, args)