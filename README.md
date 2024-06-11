# Movie Recommendation Chatbot

This repository contains a movie recommendation system integrated with a Rasa chatbot. The system recommends movies based on user input, can search for movies by genre, and provides details about specific movies. The project consists of three main components:

1. Generating Movie Embeddings (`movie_recommendation.ipynb`)
2. Initializing and Training the Rasa Model (`rasa.ipynb`)
3. Running the Chatbot Application Server (`app.py`)

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.x
- Jupyter Notebook
- Flask
- pandas
- numpy
- scikit-learn
- transformers
- torch
- Rasa
- nest-asyncio
- pyngrok (optional for local development)
- requests
- seaborn
- matplotlib

## Instructions

### Step 1: Generate Movie Embeddings

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/movie-recommendation-chatbot.git
cd movie-recommendation-chatbot
