from django.shortcuts import render
from django.views.generic import TemplateView

from googleapiclient.discovery import build
import api_token

#youtube api requests
def get_test(youtube):
    request = youtube.channels().list(
        part="statistics",
        forUsername="shafer5"
    )
    response = request.execute()
    print(response)
    return response


class Search(TemplateView):
	template_name = "search.html"
	youtube = build('youtube', 'v3', developerKey=api_token.token)

	def get(self, request):
		args = {}
		return render(request, self.template_name, args)

	def post(self, request):
		query = request.POST["search"]
		response = get_test(self.youtube)
		args = {"query": query}
		return render(request, self.template_name, args)