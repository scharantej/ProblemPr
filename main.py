 
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load the book recommendation data
books = pd.read_csv('books.csv')
ratings = pd.read_csv('ratings.csv')

# Create a dictionary of book titles and their corresponding IDs
book_titles = dict(zip(books['book_id'], books['title']))

# Create a dictionary of user IDs and their corresponding ratings for each book
user_ratings = ratings.pivot(index='user_id', columns='book_id', values='rating').fillna(0)

# Calculate the cosine similarity between users
user_similarities = user_ratings.corr(method='cosine')

# Function to generate book recommendations for a given user
def recommend_books(user_id):
    # Get the user's similarity scores with all other users
    similarities = user_similarities[user_id]

    # Get the top 10 most similar users
    top_users = similarities.nlargest(10).index

    # Get the books that the top 10 most similar users have rated highly
    recommended_books = user_ratings[top_users].mean().sort_values(ascending=False).index[:10]

    # Return the recommended books
    return recommended_books

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommendations')
def recommendations():
    # Get the user ID from the request
    user_id = request.args.get('user_id')

    # Generate book recommendations for the user
    recommended_books = recommend_books(user_id)

    # Get the titles of the recommended books
    recommended_book_titles = [book_titles[book_id] for book_id in recommended_books]

    # Render the recommendations page
    return render_template('recommendations.html', recommended_books=recommended_book_titles)

if __name__ == '__main__':
    app.run()
