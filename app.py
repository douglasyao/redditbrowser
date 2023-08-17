from flask import Flask, render_template, request
from google_search import get_posts_from_prompt, generate_summary_from_posts

app = Flask(__name__)

@app.route('/')
def serve_form():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_input():
    user_input = request.form.get('user_input', '')

    # Process the user input using your Python code
    # For example, you can return the input reversed
    posts = get_posts_from_prompt(user_input, 3)
    post_texts = [post.text for post in posts]
    if not posts:
        truncated_input = f"{user_input[:50]}..." if len(user_input) > 50 else user_input
        response = f"Sorry, no search results for `{truncated_input}`. Please try again." 
    else:
        summary = generate_summary_from_posts(posts, user_input)  
    return render_template('index.html', result=summary, post_texts=post_texts, user_input=user_input)

if __name__ == '__main__':
    app.run()
