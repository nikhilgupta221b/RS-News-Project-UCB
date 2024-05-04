import numpy as np
import requests

class UCBNewsRecommender:
    def __init__(self, categories, api_key):
        self.categories = categories
        self.api_key = api_key
        self.alpha = {category: 1 for category in categories}
        self.beta = {category: 1 for category in categories}
        self.category_counts = {category: 0 for category in categories}

    def sample_preferences(self):
        sampled_values = {category: np.random.beta(self.alpha[category], self.beta[category])
                          for category in self.categories}
        return sampled_values

    def get_top_categories(self, n=3):
        preferences = self.sample_preferences()
        # Adjusting preferences using UCB formula, incorporating actual count of recommendations per category
        adjusted_preferences = {
            category: pref + np.sqrt((2 * np.log(sum(self.category_counts.values()) + 1)) / (self.category_counts[category] + 1))
            for category, pref in preferences.items()
        }
        top_categories = sorted(adjusted_preferences, key=adjusted_preferences.get, reverse=True)[:n]
        # Incrementing the count for each category that is recommended
        for category in top_categories:
            self.category_counts[category] += 1
        return top_categories

    def update_initial_preferences(self, category, outcome):
        if outcome == 'like':
            self.alpha[category] += 3
        elif outcome == 'dislike':
            self.beta[category] += 3

    def update_preferences(self, category, outcome):
        if outcome == 'like':
            self.alpha[category] += 1
        elif outcome == 'dislike':
            self.beta[category] += 1

    def fetch_news(self, categories):
        news = {}
        url = 'https://newsapi.org/v2/top-headlines'
        headers = {'Authorization': 'Bearer ' + self.api_key}
        for category in categories:
            params = {'category': category, 'country': 'in', 'pageSize': 3}
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                articles = response.json().get('articles', [])
                news[category] = [article['title'] for article in articles]
            else:
                news[category] = ["Failed to fetch news"]
        return news
