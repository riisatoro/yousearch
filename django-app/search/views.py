from django.shortcuts import render
from django.views.generic import TemplateView

from googleapiclient.discovery import build
import api_token

#youtube api requests
def get_test(youtube, query):
    request = youtube.search().list(
    	q=query,
        part="snippet",
        type="video",
        maxResults=10
    )
    response = request.execute()

    data = []
    print(response["items"][0])
    for item in response["items"]:
    	data.append(item["id"]["videoId"])
    return data


class Search(TemplateView):
	template_name = "search.html"
	youtube = build('youtube', 'v3', developerKey=api_token.token)

	def get(self, request):
		args = {}
		return render(request, self.template_name, args)

	def post(self, request):
		query = request.POST["search"]
		video = get_test(self.youtube, query)
		args = {"query": query, "main_video": video[0], "other_video": video[1:]}
		return render(request, self.template_name, args)