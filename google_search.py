from googleapiclient.discovery import build
import pprint

my_api_key = "AIzaSyBGXiKCSjjIxnNTCz7zroVy1hr57xUb2HQ"
my_cse_id = "e19eea81c943046e2"
num_results = 10

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    res = [x['link'] for x in res['items']]
    return res

results = google_search('best sushi restaurants nyc', my_api_key, my_cse_id, num=num_results)