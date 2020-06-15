from django.shortcuts import render
from django.views.generic import TemplateView

from main.apps import *

class Search(TemplateView):
	template_name = "search.html"

	def get(self, request):
		args = {}
		return render(request, self.template_name, args)

	def post(self, request):
		query = request.POST["search"]
		print(query)
		args = {"query": query}
		return render(request, self.template_name, args)