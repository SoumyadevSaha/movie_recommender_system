import os
# from dotenv import load_dotenv
import pandas as pd
import re
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load environment variables from .env
# load_dotenv()

# Function to normalize strings (removing special characters and converting to lowercase)
def normalize_string(s):
    """
    Normalize a string by removing special characters and converting to lowercase.
    """
    return re.sub(r"[-'.,\s\t]", "", s).lower()

# Function to load movie data from CSV
def load_movie_data(csv_file_path):
    """
    Load movie data from a CSV file into a pandas DataFrame.
    """
    return pd.read_csv(csv_file_path)

# Function to fetch poster URL
def fetch_poster(movie_id):
    """
    Fetch the poster URL for a movie using The Movie Database (TMDb) API.
    """
    # api_key = os.getenv('API_KEY')  # Get API key from environment variable
    api_key = 'YOUR_API_KEY'
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US'
    
    try:
        response = requests.get(url)
        data = response.json()
        return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
    except Exception as e:
        print(f'Error fetching poster: {e}')
        return None  # Return None or a default image URL

# Function to find movie index by title
def find_movie_index(title, data):
    """
    Find the index of a movie in the DataFrame based on its title.
    """
    normalized_title = normalize_string(title)
    for idx, row in data.iterrows():
        if normalize_string(row['title']) == normalized_title:
            return idx
    return None

# Function to get top N similar movies
def get_similar_movies(title, data, similarity_matrix, top_n=10):
    """
    Get top N similar movies based on cosine similarity.
    """
    movie_idx = find_movie_index(title, data)
    if movie_idx is None:
        return None

    sim_scores = list(enumerate(similarity_matrix[movie_idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_similar_movies = sim_scores[1:top_n + 1]

    similar_movies = []
    for i in top_similar_movies:
        idx = i[0]
        movie_details = {
            'title': data.iloc[idx]['title'],
            'movie_id': int(data.iloc[idx]['movie_id']),  # Convert to standard int
            'genres': data.iloc[idx]['genres'],
            'score': float(data.iloc[idx]['score']),  # Convert to standard float
            'summary': data.iloc[idx]['summary'],
            'poster_url': fetch_poster(data.iloc[idx]['movie_id'])
        }
        similar_movies.append(movie_details)

    return similar_movies

# Function to recommend movies based on query
def recommend_movies(query, data, similarity_matrix, top_n=10):
    """
    Recommend top N movies based on the query movie title.
    If the movie is found, recommend similar movies based on cosine similarity.
    If not found, recommend top-rated movies.
    """
    movie_idx = find_movie_index(query, data)
    if movie_idx is not None:
        recommendations = get_similar_movies(query, data, similarity_matrix, top_n)
        return {'recommendations': recommendations, 'movie_found': True}
    else:
        top_movies = data.nlargest(top_n, 'score')[['title', 'movie_id', 'genres', 'score', 'summary']]
        top_movies['movie_id'] = top_movies['movie_id'].apply(int)
        top_movies['score'] = top_movies['score'].apply(float)
        
        recommendations = []
        for idx, row in top_movies.iterrows():
            recommendations.append({
                'title': row['title'],
                'movie_id': row['movie_id'],
                'genres': row['genres'],
                'score': row['score'],
                'summary': row['summary'] if 'summary' in row else '',
                'poster_url': fetch_poster(row['movie_id'])
            })
        
        return {'recommendations': recommendations, 'movie_found': False}

# Function to build the recommendation model
def build_recommendation_model(movie_data):
    """
    Build TF-IDF and cosine similarity models for movie recommendation.
    """
    tfidf = TfidfVectorizer(max_features=5000)
    tfidf_matrix = tfidf.fit_transform(movie_data['tags']).toarray()
    cosine_sim = cosine_similarity(tfidf_matrix)
    return cosine_sim

if __name__ == '__main__':
    # Load movie data
    movie_data = load_movie_data('processed_movie_data.csv')

    # Build the recommendation model
    cosine_sim = build_recommendation_model(movie_data)

    # Test the recommendation system
    recommendations = recommend_movies('The Dark Knight', movie_data, cosine_sim, top_n=10)
    print(recommendations)
