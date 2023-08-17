# redditbrowser

## requirements
```
pip3 install google-api-python-client
pip3 install requests beautifulsoup4
pip3 install flask

```

## setting up the webapp
1. install flask
2. run `python app.py` (might need to run `python3.9 app.py` if you don't have the latest python) 
3. in your browser, open http://127.0.0.1:5000/


Ask prompt through command line 
```
python3 google_search.py 'where to get hot cheetos'
```


scorer `parse_post.py` 
Have `requests` and `beautifulsoup4` installed 

To run, in the command line make sure you're in `redditbrowser`, and find the reddit post that you want to scrape. Then run `python3 parse_post <url>`. You can also just run `python3 parse_post` for the example url I used. 
