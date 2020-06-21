from django.shortcuts import render
from django.views.generic import TemplateView

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
		return render(request, self.template_name, args)