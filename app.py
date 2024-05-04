# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
from recommender import UCBNewsRecommender
import random
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv('NEWSAPIKEY')


app = Flask(__name__)

categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
recommender = UCBNewsRecommender(categories, api_key)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_categories = request.form.getlist('category')
        for category in selected_categories:
            recommender.update_initial_preferences(category, 'like')
        return redirect(url_for('news'))
    return render_template('index.html', categories=categories)

@app.route('/news')
def news():
    top_categories = recommender.get_top_categories(n=3)
    news = recommender.fetch_news(top_categories)
    news_list = [(article, category) for category, articles in news.items() for article in articles]
    random.shuffle(news_list)
    return render_template('news.html', news_list=news_list)

@app.route('/update_preference', methods=['POST'])
def update_preference():
    category = request.form['category']
    outcome = request.form['outcome']
    recommender.update_preferences(category, outcome)
    print(f"Updated values - Category: {category}, Rewards: {recommender.rewards[category]}, Counts: {recommender.counts[category]}")
    return jsonify(success=True)

if __name__ == '__main__':
    app.run()

