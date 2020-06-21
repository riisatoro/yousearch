from django.shortcuts import render
from django.views.generic import TemplateView

from googleapiclient.discovery import build
import api_token

import json
import os

from main import models

#youtube api requests
def get_test(request, youtube, query):
    query = query.lower()
    #check if query already exsists in db
    db_query = models.Request.objects.filter(query=query).exists()
    data = []
    if db_query:
        #unpack videos
        db_video = models.RequestVideo.objects.filter(request__query=query).all()
        for item in db_video:
            tmp = {
                "id": item.video.id,
                "name": item.video.name,
                "link": item.video.link,
                "iframe": item.video.iframe,
                "date": item.video.date,
                "preview": item.video.preview,
                "liked": models.UserLikedList.objects.filter(
                    user__id = request.user.id, video__id = item.video.id).all().exists()
            }
            print(tmp["liked"])
            data.append(tmp)

    else:
        #create a new query in db
        db_query = models.Request.objects.create(query=query)
        #call a youtube api to get video data by query
        request = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=13
        )
        response = request.execute()

        #parsing a data from the response
        data = []
        for item in response["items"]:
            tmp = {
                "id": item["id"]["videoId"],
                "name": item["snippet"]["title"],
                "link": "https://www.youtube.com/watch?v="+item["id"]["videoId"],
                "iframe": "https://www.youtube.com/embed/"+item["etag"],
                "date": item["snippet"]["publishedAt"].split("T")[0],
                "preview": item["snippet"]["thumbnails"]["medium"]["url"],
                "liked": models.UserLikedList.objects.filter(
                    user__id = request.user.id, video__vid_id = item["id"]["videoId"]).all().exists()
            }
            print(tmp["liked"])
            
            db_video = models.Video.objects.filter(vid_id=tmp["id"]).exists()
            if db_video:
                #connect the existed video to the new query
                db_video = models.Video.objects.filter(vid_id=tmp["id"]).get()
                db_video_query = models.RequestVideo.objects.create(request=db_query, video=db_video)
            else:
                #add a new video
                db_video = models.Video.objects.create(
                    vid_id = tmp["id"],
                    name = tmp["name"],
                    link = tmp["link"],
                    iframe = tmp["iframe"],
                    date = tmp["date"],
                    preview = tmp["preview"])
                db_video_query = models.RequestVideo.objects.create(request=db_query, video=db_video)

            data.append(tmp)

    return data


class Search(TemplateView):
    template_name = "search.html"
    youtube = build('youtube', 'v3', developerKey=api_token.token)

    def get(self, request):
        args = {"login": request.user.is_authenticated,}
        return render(request, self.template_name, args)

    def post(self, request):
        query = request.POST["search"]
        video = get_test(request, self.youtube, query)
        args = {
            "login": request.user.is_authenticated,
            "query": query,
            "main_video": video[0],
            "other_video": video[1:]
            }

        return render(request, self.template_name, args)