from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from main import models

class Main(TemplateView):
    template_name = "liked.html"

    def get(self, request):
        login = request.user.is_authenticated
        user = request.user
        is_list = False
        data = []
        message = ""

        if login:
            video_list = models.UserLikedList.objects.filter(user__id = user.id)
            if video_list.exists():
                is_list = True
                for item in video_list:
                    tmp = {
                        "id": item.video.vid_id,
                        "name": item.video.name,
                        "link": item.video.link,
                        "iframe": item.video.iframe,
                        "date": item.video.date,
                        "preview": item.video.preview,
                        "liked": True
                    }
                    data.append(tmp)
            else:
                message = "Your list is empty :("

        else:
            message = "Please, log in or create an account to add videos to the liked list"
        
        args = {
            "login": login, 
            "message": message,
            "is_list": is_list,
            "video": data,
            }
        return render(request, self.template_name, args)


    def post(self, request):
        return render(request, self.template_name, args)


class NewLiked(TemplateView):
    template_name = "liked.html"

    def get(self, request):
        if request.user.is_authenticated:
            login_message = "Welcome!"
        else:
            login_message = "Please, log in or create an account to add videos to the liked list"
        args = {"login_message": login_message}
        return render(request, self.template_name, args)


    def post(self, request):
        liked = request.POST["videoId"]
        query = request.POST["query"]
        user = models.AuthUser.objects.filter(id=request.user.id)

        if user.exists():
            db_video = models.UserLikedList.objects.filter(
                user__id=request.user.id, video__vid_id=liked)

            if db_video.exists():
                db_video.delete()
            else:
                video = models.Video.objects.get(vid_id=liked)  
                models.UserLikedList.objects.create(
                user=user.get(), video=video)
        else:
            return redirect("/auth")
        return redirect("/liked")