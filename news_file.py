
import requests
import json

# Saved in local file
import keys
from newsapi import NewsApiClient
from datetime import datetime, timedelta

# Function to get formatted dates
def get_formatted_dates():
    today = datetime.now().strftime("%Y-%m-%d")  # Format: YYYY:MM:DD
    yesterday = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
    return today, yesterday

# Example usage

# Get NewsApi Key, Saved in different file

newsapi = NewsApiClient(api_key=keys.get_news_api_key())

def get_news_from_keyword(keyword):
    today, yesterday = get_formatted_dates()
    all_articles = newsapi.get_everything(q=keyword,
                                      from_param=yesterday,
                                      to=today,
                                      language='en',
                                      sort_by='popularity',
                                      page=1)
    titles=[]
    if all_articles["articles"]:
        for article in all_articles["articles"]:
            titles.append(article['title'])
    return titles[:10]

