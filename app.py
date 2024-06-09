from flask import Flask, request, jsonify, render_template, make_response
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModel
import torch
import pickle
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Load the embeddings from the file
with open('movie_embeddings.pkl', 'rb') as f:
    movies_metadata_cleaned = pickle.load(f)

# Ensure the 'popularity' column is numeric
movies_metadata_cleaned['popularity'] = pd.to_numeric(movies_metadata_cleaned['popularity'], errors='coerce')

# Initialize tokenizer and model (required for generating embeddings for new queries)
tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
model = AutoModel.from_pretrained('bert-base-uncased')

def get_embeddings(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).detach().numpy()
    return embeddings.flatten()

def recommend_movies(movie_title, num_recommendations=5):
    movie_idx = movies_metadata_cleaned[movies_metadata_cleaned['title'].str.lower() == movie_title.lower()]
    if not movie_idx.empty:
        movie_idx = movie_idx.index[0]
        movie_embedding = movies_metadata_cleaned.loc[movie_idx, 'embeddings']
        similarities = cosine_similarity([movie_embedding], list(movies_metadata_cleaned['embeddings']))
        similar_indices = similarities.argsort()[0][-num_recommendations-1:-1][::-1]
        return movies_metadata_cleaned.iloc[similar_indices]['title'].tolist()
    else:
        return []

def search_movies_by_genre(genre):
    results = movies_metadata_cleaned[movies_metadata_cleaned['genres'].apply(lambda x: genre.lower() in [g.lower() for g in x])]
    # Sort by popularity and get the top 5 movies
    top_movies = results.sort_values(by='popularity', ascending=False).head(5)
    return top_movies['title'].tolist()

def get_movie_details(movie_title):
    important_columns = ['title', 'genres', 'release_date', 'overview', 'popularity']
    movie = movies_metadata_cleaned[movies_metadata_cleaned['title'].str.lower() == movie_title.lower()]
    if not movie.empty:
        movie_details = movie[important_columns].iloc[0]
        formatted_details = (
            f"<br>"
            f"<b>Genres:</b> {', '.join(movie_details['genres'])}<br>"
            f"<b>Release Date:</b> {movie_details['release_date']}<br>"
            f"<b>Overview:</b> {movie_details['overview']}<br>"
            f"<b>Popularity:</b> {movie_details['popularity']}"
        )
        return formatted_details
    else:
        return "Sorry, I couldn't find details for the specified movie."



@app.route('/')
def index():
    response = make_response(render_template('index.html'))
    response.headers['Cache-Control'] = 'no-store'
    return response

def parse_rasa_response(rasa_response):
    logging.debug(f"Rasa response: {rasa_response}")
    intent = rasa_response.get('intent', {}).get('name', 'unknown')
    entities = {entity['entity']: entity['value'] for entity in rasa_response.get('entities', [])}
    return intent, entities

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    user_input = data.get('user_input', '')
    if not user_input:
        return jsonify({'error': 'No input provided'}), 400

    # Send user input to Rasa NLU
    rasa_url = "http://localhost:5005/model/parse"
    response = requests.post(rasa_url, json={"text": user_input})
    if response.status_code != 200:
        return jsonify({'error': 'Failed to get a response from Rasa'}), response.status_code

    rasa_response = response.json()
    intent, entities = parse_rasa_response(rasa_response)

    if intent == 'get_recommendation':
        movie_title = entities.get('movie_title', '')
        recommendations = recommend_movies(movie_title)
        if recommendations:
            return jsonify({'response': f"If you liked {movie_title}, you might also enjoy: {', '.join(recommendations)}"})
        else:
            return jsonify({'response': f"Sorry, I couldn't find recommendations for {movie_title}."})
    elif intent == 'search_by_genre':
        genre = entities.get('genre', '')
        movies = search_movies_by_genre(genre)
        if movies:
            return jsonify({'response': f"Here are some {genre} movies: {', '.join(movies)}"})
        else:
            return jsonify({'response': f"Sorry, I couldn't find any movies in the {genre} genre."})
    elif intent == 'get_movie_details':
        movie_title = entities.get('movie_title', '')
        details = get_movie_details(movie_title)
        if details:
            return jsonify({'response': f"Details for {movie_title}: {details}"})
        else:
            return jsonify({'response': f"Sorry, I couldn't find details for {movie_title}."})
    elif intent == 'greet':
        return jsonify({'response': "Hello! How can I assist you with movies today?"})
    elif intent == 'goodbye':
        return jsonify({'response': "Goodbye! Have a great day!"})
    else:
        return jsonify({'response': "I'm sorry, I didn't understand that. Can you please specify if you want recommendations, details, or search by genre?"})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
