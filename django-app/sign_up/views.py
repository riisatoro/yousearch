from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import login, logout, authenticate

from .forms import RegisterForm


class Main(TemplateView):
	template_name = "auth.html"

	def get(self, request):
		args = {"login":RegisterForm()}
		return render(request, self.template_name, args)

	def post(self, request):
		form = RegisterForm(request.POST)
		if form.is_valid():
			print("[VALID]")
			form.save()
			return redirect("/account")
		else:
			args = {"login":RegisterForm()}
			return render(request, self.template_name, args)


class Registration(TemplateView):
	def get(self, request):
		args = {"login":RegisterForm()}
		return render(request, self.template_name, args)

	def post(self, request):
		form = RegisterForm(request.POST)
		if form.is_valid():
			#add new user
			form.save()

			#login user
			username=request.POST["username"]
			password=request.POST["password1"]
			user = authenticate(request, username=username, password=password)
			login(request, user)

			return redirect("/")
		else:
			return redirect("/auth")


class Login(TemplateView):
	def get(self, request):
		args = {"login":RegisterForm()}
		return render(request, self.template_name, args)

	def post(self, request):
		username=request.POST["username"]
		password=request.POST["password1"]
		user = authenticate(request, username=username, password=password)		
		login(request, user)
		return redirect("/")


class Logout(TemplateView):
	def get(self, request):
		logout(request)
		return redirect("/")

	def post(self, request):
		logout(request)
		return redirect("/")