from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

import requests
from datetime import datetime, timedelta


class TrendingReposView(APIView):
    """
    A view that returns the count and list of repos written in programming languages for trending repos in JSON.
    """
    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        from_date = (datetime.now() - timedelta(days=30)).date()
        repos = requests.get("https://api.github.com/search/repositories", \
                    params={'q': 'created:>' + from_date.strftime("%Y-%m-%d"), \
                    'sort': 'stars', 'order': 'desc', 'per_page': 100, 'page': 1},\
                    headers={'accept': 'application/vnd.github.v3+json'}).json()['items']
        response = {}
        for repo in repos:
            repo_name = repo['full_name']
            repo_language = repo['language']
            if repo_language in response.keys():
                response[repo_language]['number_repos'] += 1
                response[repo_language]['repos'].append(repo_name)
            else:
                response[repo_language] = {'number_repos': 1, 'repos': [repo_name,]}
        return Response({"result": response})