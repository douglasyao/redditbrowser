
class Post:
    ''' a Reddit post object '''
    def __init__(self, text, author, link, date, num_upvotes, num_comments):
        self.text = text
        self.author = author
        self.link = link
        self.date = date 
        self.num_upvotes = num_upvotes 
        self.num_comments = num_comments 

    def __repr__(self):
        return f"Post(author={self.author}, date={self.date})\n{self.num_upvotes} Karma\n{self.text}\n"