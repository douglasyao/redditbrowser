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

def generate_json_from_url(url):
    openai.api_key = CHAT_GPT_API_KEY
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )
    submission = reddit.submission(url=url)
    submission.comments.replace_more(limit=None)
    text = submission.title + submission.selftext
    comments = []
    for comment in submission.comments:
        comments.append(comment.body)
    comments = '---'.join(comments)
    system_message = 'You are given a prompt that usually (but not always) starts with a question. The user will input a sequence of comments that are separated by the "---" symbol. Your job is to evaluate all comments and return all independent phrases from the comments that either directly answer the question in the prompt, or are related to the prompt in some way. The phrases should be as short and concise as possible. If multiple different comments include the same phrase, then return the phrase only once. Return every possible phrase even if it occurs only once. The prompt is: "{}"'.format(text)
    
    response = openai.ChatCompletion.create(
       model="gpt-3.5-turbo",
       messages=[
           {"role": "system", "content": system_message},
           {"role": "user", "content": comments}
       ]
    )
    assistant_reply = response['choices'][0]['message']['content']
    
    system_message2 = 'You are given a list of phrases separated by commas. The user will input a sequence of comments that are separated by the "---" symbol. Your job is to output a json file, where the keys are the individual phrases, and the value for each phrase is all strings containing the phrase in the comments. Each string should be an exact quote (word for word) from a comment that includes some context and/or sentiment about the phrase if possible, such as whether the comment likes or dislikes the phrase. Include exactly one phrase per string. If a string contains multiple phrases, then split the string so each substring contains exactly one phrase. Include only one comment maximum in each string. If the comment does not mention any phrase in the list, then skip the comment. The list of phrases is: "{}"'.format(assistant_reply)
    
    response = openai.ChatCompletion.create(
       model="gpt-3.5-turbo",
       messages=[
           {"role": "system", "content": system_message2},
           {"role": "user", "content": comments}
       ]
    )
    assistant_reply2 = response['choices'][0]['message']['content']
    return(assistant_reply2)


if __name__ == "__main__":
    if (len(sys.argv) == 2):
        prompt = sys.argv[1]
        posts = get_posts_from_prompt(prompt)
        generate_summary_from_posts(posts, prompt)
        print(posts)