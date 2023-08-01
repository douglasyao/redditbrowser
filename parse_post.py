import requests
from bs4 import BeautifulSoup
import sys

# https://www.reddit.com/r/StardewValley/comments/hudgy3/who_is_the_best_and_worst_characters_in_stardew/

def score_post(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        html_content = response.text
    else:
        print("Failed to fetch data. Status code:", response.status_code)


    soup = BeautifulSoup(html_content, "html.parser")
    post_info = soup.find("shreddit-post")
    # Find all post containers
    p_elements = soup.find_all("p")
    author_username = post_info['author']
    post_link = post_info['content-href']
    post_comment_count = post_info['comment-count']
    post_upvote_count = post_info['score']
    post_timestamp = soup.find("faceplate-timeago")['ts'][:10]

    full_text = ''
    for paragraph in p_elements:
        full_text += paragraph.text 

    info_dictionary = { 'date': post_timestamp, 
                        'upvotes': post_upvote_count, 
                        'comment_count': post_comment_count,
                        'author': author_username, 
                        'link': post_link, 
                        'text':full_text}
    print(info_dictionary)
    return info_dictionary


if __name__ == "__main__":
    if (len(sys.argv) == 2):  
        #TODO handle prompt 
        url = sys.argv[1]
        score_post(url)
    else:
        score_post("https://www.reddit.com/r/SkincareAddiction/comments/ibnor5/review_cosrx_snail_mucin_essence_lives_up_to_the/")
