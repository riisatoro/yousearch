from django.shortcuts import render
from django.views.generic import TemplateView

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

class Main(TemplateView):
	template_name = "auth.html"

	def get(self, request):
		args = {"login":UserCreationForm()}
		return render(request, self.template_name, args)

	def post(self, request):
		pass