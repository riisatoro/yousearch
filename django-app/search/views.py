from django.shortcuts import render
from django.views.generic import TemplateView

from googleapiclient.discovery import build
import api_token

import json
import os

from main import models

def get_from_youtube(youtube,query):
    #call a youtube api to get video data by query
    request = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=13
        )
    response = request.execute()
    return response


def get_video_data(user, youtube, query):
    #save new queries, get videos from youtube
    #or get old queries and videos of it
    query = query.lower()
    
    data = []
    #check if query already exsists in db
    db_query = models.Request.objects.filter(query=query)
    if db_query.exists():
        #unpack videos
        db_video = models.RequestVideo.objects.filter(request__query=query)
        for item in db_video.all():
            tmp = {
                "id": item.video.vid_id,
                "name": item.video.name,
                "link": item.video.link,
                "iframe": item.video.iframe,
                "date": item.video.date,
                "preview": item.video.preview,
                "liked": models.UserLikedList.objects.filter(
                    user__id = user.id, video__id = item.video.id).all().exists()
            }
            data.append(tmp)

    else:
        #create a new user's query in db
        db_query = models.Request.objects.create(query=query)
        response = get_from_youtube(youtube, query)
        
        #parsing a data from the response
        for item in response["items"]:
            tmp = {
                "id": item["id"]["videoId"],
                "name": item["snippet"]["title"],
                "link": "https://www.youtube.com/watch?v="+item["id"]["videoId"],
                "iframe": "https://www.youtube.com/embed/"+item["etag"],
                "date": item["snippet"]["publishedAt"].split("T")[0],
                "preview": item["snippet"]["thumbnails"]["medium"]["url"],
                "liked": models.UserLikedList.objects.filter(
                    user__id = user.id, video__vid_id = item["id"]["videoId"]).all().exists()
            }

            #if video alreay in database then just connect it to the new user's query
            db_video = models.Video.objects.filter(vid_id=tmp["id"])
            
            if db_video.exists():
                #connect old video to the new query
                models.RequestVideo.objects.create(
                    request=db_query, video=db_video.get())
            else:
                #add a new video
                db_video = models.Video.objects.create(
                    vid_id = tmp["id"],
                    name = tmp["name"],
                    link = tmp["link"],
                    iframe = tmp["iframe"],
                    date = tmp["date"],
                    preview = tmp["preview"])

                #connect new video to the new query
                models.RequestVideo.objects.create(request=db_query, video=db_video)

            data.append(tmp)

    return data


class Search(TemplateView):
    template_name = "search.html"
    youtube = build('youtube', 'v3', developerKey=api_token.token)

    def get(self, request):
        if request.user.is_authenticated():
            return redirect("/liked")
        else:
            return redirect("/")

    def post(self, request):
        query = request.POST["search"]
        video = get_video_data(request.user, self.youtube, query)
        print(video)

        if len(video) > 0:
            main_video = video[0]
            other_video = video[1:]
            error = False
            error_msg = None
        else:
            error = True
            error_msg = "Sorry, but YouTube can't find any video by Your query :("
            main_video = None
            other_video = None

        args = {
            "error": error,
            "error_msg": error_msg,
            "login": request.user.is_authenticated,
            "query": query,
            "main_video": main_video,
            "other_video": other_video,
            }

        return render(request, self.template_name, args)