from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from main import models

class Main(TemplateView):
	template_name = "liked.html"

	def get(self, request):
		login = request.user.is_authenticated
		if login:
			login_message = "Welcome!"
		else:
			login_message = "Please, log in or create an account to add videos to the liked list"
		
		args = {"login": login, "login_message": login_message}
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

		print(liked)

		db_video = models.UserLikedList.objects.filter(
			user__id=request.user.id, video__vid_id=liked)

		if db_video.exists():
			db_video.delete()
		else:
			video = models.Video.objects.get(vid_id=liked)
			user = models.AuthUser.objects.get(id=request.user.id)
			models.UserLikedList.objects.create(
			user=user, video=video)
		
		return redirect("/liked")