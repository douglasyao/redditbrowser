from googleapiclient.discovery import build
import pprint
from parse_post import create_post_from_url
import sys
from config import * 
import openai 


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    res = [x['link'] for x in res['items']]
    return res

def get_posts_from_prompt(prompt, num_results=10):
    posts = []
    post_urls = google_search(prompt, GOOGLE_API_KEY, GOOGLE_CSE_ID, num=num_results)
    for post_url in post_urls:
        post = create_post_from_url(post_url)
        posts.append(post)
    return posts

def generate_summary_from_posts(posts, prompt):
    openai.api_key = CHAT_GPT_API_KEY
    prompt_start = f"Given these following opinions, what can we deduce about: {prompt}?"
    list_of_post_texts = []
    
    for i, post in enumerate(posts):
        prompt_start += f"\n{i}. {post.text}"
        list_of_post_texts.append(post.text)
    
    response = openai.Completion.create(
        engine="text-davinci-002",  # Choose the engine you want to use
        prompt=prompt,
        temperature=0.2,
        max_tokens=150,  # Set the maximum length of the response
    )
    print("response:\n", response)
    # Extract the response from the API call
    chat_gpt_response = response.choices[0].text.strip()
    return chat_gpt_response



if __name__ == "__main__":
    if (len(sys.argv) == 2):
        prompt = sys.argv[1]
        posts = get_posts_from_prompt(prompt)
        generate_summary_from_posts(posts, prompt)
        print(posts)