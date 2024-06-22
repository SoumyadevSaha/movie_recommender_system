# Movie Recommender System

## Introduction
Welcome to the Movie Recommender System project! This project utilizes a content-based recommender system to suggest movies based on user preferences. The backend is hosted on [PythonAnywhere](https://shaxx69.pythonanywhere.com/), and the frontend is hosted on [Netlify](https://movie-verse-soumya.netlify.app/).

## Table of Contents
- [What is a Recommender System?](#what-is-a-recommender-system)
- [Types of Recommender Systems](#types-of-recommender-systems)
  - [Content Based](#content-based)
  - [Collaborative Filtering Based](#collaborative-filtering-based)
  - [Hybrid](#hybrid)
- [Project Flow](#project-flow)
- [Data Preprocessing](#data-preprocessing)
- [Recommender System Logic](#recommender-system-logic)
- [TF-IDF and Cosine Similarity](#tf-idf-and-cosine-similarity)
- [Folder Structure](#folder-structure)
- [Running the Project](#running-the-project)

## What is a Recommender System?
A recommender system predicts the preference of a user for a particular item. Popular platforms like Spotify, YouTube, Facebook, Instagram, and Netflix use recommender systems to enhance user experience by suggesting relevant content.

## Types of Recommender Systems
### Content Based
Content-based recommender systems suggest items similar to those a user has liked in the past, based on item features. Tags and keywords are used to capture the content similarity.

### Collaborative Filtering Based
Collaborative filtering systems recommend items based on the preferences of similar users. If users A and B have similar tastes, a movie liked by A is likely to be recommended to B.

### Hybrid
Hybrid recommender systems combine content-based and collaborative filtering approaches to leverage the strengths of both methods.

## Project Flow
1. **Data Preprocessing**: Clean and prepare the data.
2. **Model Building**: Develop a model based on the preprocessed data.
3. **Frontend Development**: Create a user-friendly interface.
4. **Backend Integration**: Seamlessly integrate the model with the web application.
5. **Deployment**: Host the application online.

## Data Preprocessing
The preprocessing steps are implemented in `preprocessor.py` and include:
1. Merging two datasets (`tmdb_5000_movies.csv` and `tmdb_5000_credits.csv`) accessed from [this Kaggle dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata/).
2. Removing unwanted columns and renaming columns for clarity.
3. Converting genres, keywords, and cast to lists of strings.
4. Removing stopwords from the overview.
5. Creating a combined tags column from genres, keywords, cast, and overview.
6. Converting all tags to lowercase and combining them into a single string.
7. Saving the processed data to `processed_movie_data.csv`.

```python
# Example preprocessing function
def preProcessData(movie_data, creds_data):
    # ... (code from preprocessor.py)
    return movie_data
```

## Recommender System Logic
The logic of the recommender system is implemented in `recommender.py`. Key functions include:

### Normalizing Strings
Converting strings to lowercase and removing special characters to standardize data.

```python
def normalize_string(s):
    return re.sub(r"[-'.,\s\t]", "", s).lower()
```

### Fetching Movie Posters
Fetching movie posters using The Movie Database (TMDb) API.

```python
def fetch_poster(movie_id):
    api_key = 'YOUR_API_KEY'
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US'
    # ... (API request and error handling)
    return poster_url
```

### Finding Movie Index
Finding the index of a movie in the DataFrame based on its title.

```python
def find_movie_index(title, data):
    normalized_title = normalize_string(title)
    for idx, row in data.iterrows():
        if normalize_string(row['title']) == normalized_title:
            return idx
    return None
```

### Getting Similar Movies
Getting top N similar movies based on cosine similarity.

```python
def get_similar_movies(title, data, similarity_matrix, top_n=10):
    movie_idx = find_movie_index(title, data)
    if movie_idx is None:
        return None
    sim_scores = list(enumerate(similarity_matrix[movie_idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_similar_movies = sim_scores[1:top_n + 1]
    # ... (code to fetch movie details and posters)
    return similar_movies
```

### Recommending Movies
Recommending top N movies based on the query movie title.

```python
def recommend_movies(query, data, similarity_matrix, top_n=10):
    movie_idx = find_movie_index(query, data)
    if movie_idx is not None:
        recommendations = get_similar_movies(query, data, similarity_matrix, top_n)
        return {'recommendations': recommendations, 'movie_found': True}
    else:
        top_movies = data.nlargest(top_n, 'score')[['title', 'movie_id', 'genres', 'score']]
        # ... (code to fetch movie details and posters)
        return {'recommendations': recommendations, 'movie_found': False}
```

### Building the Recommendation Model
Building the TF-IDF model and computing cosine similarity.

```python
def build_recommendation_model(movie_data):
    tfidf = TfidfVectorizer(max_features=5000)
    tfidf_matrix = tfidf.fit_transform(movie_data['tags']).toarray()
    cosine_sim = cosine_similarity(tfidf_matrix)
    return cosine_sim
```

## TF-IDF and Cosine Similarity
TF-IDF (Term Frequency-Inverse Document Frequency) is used to convert textual data into numerical vectors, highlighting the importance of words in the documents. Cosine similarity measures the similarity between two vectors, indicating how similar two movies are based on their tags.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def build_recommendation_model(movie_data):
    tfidf = TfidfVectorizer(max_features=5000)
    tfidf_matrix = tfidf.fit_transform(movie_data['tags']).toarray()
    cosine_sim = cosine_similarity(tfidf_matrix)
    return cosine_sim
```

## Folder Structure
```bash
.
├── app.py
├── recommender.py
├── processed_movie_data.csv
├── client
│   ├── index.html
│   ├── styles.css
│   ├── script.js
├── requirements.txt
```

## Running the Project
1. **Clone the Repository**: Clone the repository to your local machine.
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```
2. **Install Dependencies**: Install required Python packages.
    ```bash
    pip install -r requirements.txt
    ```
3. **Download the Data**: Download the `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` files from [this Kaggle dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata/) and place them in the project directory.
4. **Preprocess Data**: Run the preprocessing script to generate `processed_movie_data.csv`.
    ```bash
    python preprocessor.py
    ```
5. **Run the Flask App**: Start the Flask server.
    ```bash
    python app.py
    ```
6. **Access the Application**: Open your browser and go to `http://localhost:6543`.
