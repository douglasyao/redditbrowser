from googleapiclient.discovery import build
import pprint
from parse_post import create_post_from_url
import sys
from config import * 

num_results = 10

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    res = [x['link'] for x in res['items']]
    return res

def get_posts_from_prompt(prompt):
    posts = []
    post_urls = google_search(prompt, GOOGLE_API_KEY, GOOGLE_CSE_ID, num=num_results)
    for post_url in post_urls:
        post = create_post_from_url(post_url)
        posts.append(post)
    return posts

if __name__ == "__main__":
    if (len(sys.argv) == 2):
        prompt = sys.argv[1]
        posts = get_posts_from_prompt(prompt)
        print(posts)