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

Open the Jupyter Notebook movie_recommendation.ipynb:

'''bash
複製程式碼
jupyter notebook movie_recommendation.ipynb
Execute all cells in movie_recommendation.ipynb to generate movie embeddings and save them to movie_embeddings.pkl.

### Step 2: Initialize and Train the Rasa Model
Open the Jupyter Notebook rasa.ipynb:

'''bash
複製程式碼
jupyter notebook rasa.ipynb
Execute all cells in rasa.ipynb to initialize, train the Rasa model, and start the Rasa server.

### Step 3: Run the Chatbot Application Server
Ensure the Rasa server is running. You can start the Rasa server from the command line if it's not already running:

'''bash
複製程式碼
rasa run --enable-api --cors "*" --port 5005
Run the Flask application server:

'''bash
複製程式碼
python app.py
Open your browser and navigate to http://localhost:5000 to interact with the chatbot.

Repository Structure
plaintext
複製程式碼
movie-recommendation-chatbot/
├── data/
│   └── movies_metadata.csv
├── movie_recommendation.ipynb
├── rasa.ipynb
├── app.py
├── templates/
│   └── index.html
├── static/
│   └── css/
│       └── styles.css
├── README.md

Usage
Movie Recommendations: Ask the bot to recommend movies similar to a given movie. Example: "Can you recommend a movie similar to Toy Story?"
Search by Genre: Ask the bot to show movies of a particular genre. Example: "Show me some action movies."
Movie Details: Ask the bot for details about a specific movie. Example: "Tell me about the movie Inception."
Notes
Ensure the dataset movies_metadata.csv is placed in the data directory.
Modify paths in the scripts if necessary to match your local directory structure.
The embeddings generation and Rasa model training might take some time depending on your hardware.
Contributing
Feel free to submit issues or pull requests if you have suggestions or improvements.

License
This project is licensed under the MIT License - see the LICENSE file for details.
