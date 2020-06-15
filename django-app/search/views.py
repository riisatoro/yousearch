from django.shortcuts import render
from django.views.generic import TemplateView

class Search(TemplateView):
	template_name = "search.html"

	def get(self, request):
		args = {}
		return render(request, self.template_name, args)

	def post(self, request):
		args = {}
		return render(request, self.template_name, args)