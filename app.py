from flask import Flask, request, jsonify
import pandas as pd
import os
from recommender import recommend_movies, build_recommendation_model
from flask_cors import CORS  # Import CORS from flask_cors module

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes of the Flask app

# LOAD DATA
movie_data = pd.read_csv('processed_movie_data.csv')

# LOAD THE COSINE SIMILARITY MATRIX
cosine_sim = build_recommendation_model(movie_data)

@app.route('/')
def home():
    return "Welcome to the backend of Movie Verse API ver1. Go to '/recommend' rroute."

@app.route('/recommend', methods=['GET'])
def recommend():
    """Recommend movies based on the provided title."""
    title = request.args.get('title')
    if not title:
        return jsonify({'error': 'Title parameter is required'}), 400
    
    recommendations = recommend_movies(title, movie_data, cosine_sim, top_n=51)
    if recommendations:
        return jsonify(recommendations)
    else:
        return jsonify({'error': 'Movie not found'}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 6543))
    app.run(debug=False, host='0.0.0.0', port=port)
