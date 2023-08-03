import requests
from post import Post
from bs4 import BeautifulSoup
import sys

TIMESTAMP_STRING_LENGTH = 10  # format: MM-DD-YYYY

''' Given a Reddit post link, we return a new Post object'''
def create_post_from_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        html_content = response.text
    else:
        print("Failed to fetch data. Status code:", response.status_code)

    soup = BeautifulSoup(html_content, "html.parser")
    post_info = soup.find("shreddit-post")

    p_elements = soup.find_all("p")

    full_text = ''
    for paragraph in p_elements:
        full_text += paragraph.text

    author_username = post_info['author']
    post_link = post_info['content-href']
    post_comment_count = post_info['comment-count']
    post_upvote_count = post_info['score']
    post_timestamp = soup.find(
        "faceplate-timeago")['ts'][:TIMESTAMP_STRING_LENGTH]
    post = Post(text=full_text, author=author_username, link=post_link,
                date=post_timestamp, num_upvotes=post_upvote_count, num_comments=post_comment_count)
    return post


# if __name__ == "__main__":
#     if (len(sys.argv) == 2):
#         #TODO handle prompt
#         url = sys.argv[1]
#         score_post(url)
#     else:
#         score_post("https://www.reddit.com/r/SkincareAddiction/comments/ibnor5/review_cosrx_snail_mucin_essence_lives_up_to_the/")
