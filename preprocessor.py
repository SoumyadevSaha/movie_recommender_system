## Download the 'tmdb_5000_movies.csv' and 'tmdb_5000_credits.csv' from the Kaggle website
## Link : https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata/

import pandas as pd
import ast
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

def genKeyConverter(genres):
    '''Convert the genres and keywords from objects to list of strings'''
    obj = ast.literal_eval(genres) # the genres is in string format, so convert it to object first
    genre_lst = []
    for _dict in obj:
        genre_lst.append(_dict['name'])
    return genre_lst

def castConverter(casts):
    '''Convert the cast from objects to list of strings'''
    obj = ast.literal_eval(casts)
    cast_lst = []
    for _dict in obj[:3]:
        cast_lst.append(_dict['name'])
    return cast_lst

def removeStopWords(string):
    '''Remove the stop words from the string'''
    stop_words = set(stopwords.words('english'))
    words = string.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return filtered_words

def preProcessData(movie_data, creds_data):
    '''Preprocess the data'''
    # Step 1 : Merge the two datasets on the 'id' column
    movie_data.rename(columns={'id':'movie_id'}, inplace=True)
    movie_data = movie_data.merge(creds_data, on='movie_id')

    # Step 2 : Remove unwanted columns
    columns_to_keep = ['genres', 'movie_id', 'keywords', 'title_x', 'overview', 'vote_average', 'cast']
    movie_data = movie_data[columns_to_keep]
    movie_data.rename(columns={'title_x':'title'}, inplace=True)

    # Step 3 : our new dataframe shall contain the columns : movie_id, title, tags, score. We need to somehow efficiently merge overview, genres, keywords and cast (for cast, join only the top 3-5 casts)
    movie_data.rename(columns={'vote_average':'score'}, inplace=True)
    movie_data.dropna(inplace=True)
    movie_data['genres'] = movie_data['genres'].apply(genKeyConverter)
    movie_data['keywords'] = movie_data['keywords'].apply(genKeyConverter)
    movie_data['cast'] = movie_data['cast'].apply(castConverter)
    # But before that, let's store the initial overview as a summary of the movie
    movie_data['summary'] = movie_data['overview']
    movie_data['overview'] = movie_data['overview'].apply(removeStopWords)

    # Step 4 : Finally, let's remove any spaces in the tags (to avoid confusion) [change "Sam Walker" to "SamWalker"]
    movie_data['genres2'] = movie_data['genres'].apply(lambda x:[i.replace(" ", "") for i in x])
    movie_data['cast'] = movie_data['cast'].apply(lambda x:[i.replace(" ", "") for i in x])
    movie_data['keywords'] = movie_data['keywords'].apply(lambda x:[i.replace(" ", "") for i in x])

    # Step 5 : Let's merge the tags into one column
    movie_data['tags'] = movie_data['genres2'] + movie_data['cast'] + movie_data['keywords'] + movie_data['overview']
    # And also, let's convert everything (the tags) to lowercase
    movie_data['tags'] = movie_data['tags'].apply(lambda x:[i.lower() for i in x])

    # Step 6 : Finally, we shall remove the overview, cast and keywords columns
    movie_data = movie_data[['movie_id', 'title', 'genres', 'score', 'tags', 'summary']]
    # Combine the tags list into a single string for each movie
    movie_data['tags'] = movie_data['tags'].apply(lambda x: " ".join(x))

    # FINALLY RETURN THE PROCESSED DATA
    return movie_data

if __name__ == '__main__':
    # Load the movie data
    movie_data = pd.read_csv('tmdb_5000_movies.csv')
    creds_data = pd.read_csv('tmdb_5000_credits.csv')
    # Preprocess the data
    movie_data = preProcessData(movie_data, creds_data)
    # Save the processed data
    movie_data.to_csv('processed_movie_data.csv', index=False)
    print("Data Preprocessing Completed!")
