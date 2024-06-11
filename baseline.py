import pandas as pd

# Load the original dataset
file_path = './data/movies_metadata.csv'  # Adjust the path to your local file
movies_metadata = pd.read_csv(file_path, low_memory=False)

# Convert 'popularity' to numeric and 'genres' to list
movies_metadata['popularity'] = pd.to_numeric(movies_metadata['popularity'], errors='coerce')

# Function to parse genres from string to list
def parse_genres(genres_str):
    try:
        genres_list = eval(genres_str)
        return [genre['name'] for genre in genres_list]
    except:
        return []

# Apply the genre parsing function
movies_metadata['genres'] = movies_metadata['genres'].apply(parse_genres)

# Function to find top 10 science fiction action movies
def find_top_sci_fi_action_movies(movies_metadata):
    def is_sci_fi_action(genres):
        genres_lower = [g.lower() for g in genres]
        return 'science fiction' in genres_lower and 'action' in genres_lower

    # Filter movies with both 'science fiction' and 'action' genres
    sci_fi_action_movies = movies_metadata[movies_metadata['genres'].apply(is_sci_fi_action)]

    # Sort by popularity and get the top 10 movies
    top_sci_fi_action_movies = sci_fi_action_movies.sort_values(by='popularity', ascending=False).head(10)

    # Select important columns to display
    important_columns = ['title', 'genres', 'release_date', 'popularity']
    return top_sci_fi_action_movies[important_columns]

# Find and print the top 10 science fiction action movies
top_sci_fi_action_movies = find_top_sci_fi_action_movies(movies_metadata)
print(top_sci_fi_action_movies)
