
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.exceptions import SpotifyException
from requests.exceptions import HTTPError
import matplotlib.pyplot as plt
import numpy as np
import requests
from time import sleep

# Spotify API Setup
client_id = "8c662d4fe4f049c9a479cc16d2f05e76"
client_secret = "d4450a692f7f4263888dc66f21cf8d43"

# Using Client Credentials Flow to obtain access token
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt
import numpy as np
import time


# Function to fetch song details
def find_song(song_name):
    """Searches for a song on Spotify and returns its details."""
    result = sp.search(q=song_name, limit=1, type='track')
    if result['tracks']['items']:
        return result['tracks']['items'][0]
    return None

# Function to fetch song recommendations
def recommend_songs(song_id):
    """Recommends similar songs based on a given song ID."""
    try:
        results = sp.recommendations(seed_tracks=[song_id], limit=5)
        if results['tracks']:
            return results['tracks']
        else:
            st.warning(f"No recommendations found for song {song_id}")
            return None
    except spotipy.exceptions.SpotifyException as e:
        st.error(f"Spotify API error (recommendations): {e}")
        time.sleep(2)  # Adding delay to avoid hitting rate limits
        return None
    except Exception as e:
        st.error(f"Error fetching recommendations: {e}")
        return None

# Function to plot radar chart for song features (Danceability, Energy, etc.)
def plot_radar_chart(features):
    """Plot radar chart for song features like danceability, energy, etc."""
    categories = ['Danceability', 'Energy', 'Valence', 'Acousticness']
    values = [features.get(category.lower(), 0) for category in categories]
    
    # Radar chart setup
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    values += values[:1]  # To make the chart a closed loop
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='b', alpha=0.25)
    ax.plot(angles, values, color='b', linewidth=2)

    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)

    st.pyplot(fig)

# Streamlit UI
st.title("Spotify Song Explorer and Recommender")

song_input = st.text_input("Enter a Song Name", "")

if song_input:
    # Find the song
    song = find_song(song_input)

    if song:
        # Display song details
        st.write(f"**Song Name:** {song['name']}")
        st.write(f"**Artist:** {song['artists'][0]['name']}")
        st.write(f"**Album:** {song['album']['name']}")
        st.write(f"**Popularity:** {song['popularity']}")
        st.write(f"**Release Date:** {song['album']['release_date']}")
        
        # Display album cover image
        st.image(song['album']['images'][0]['url'], width=300)
        
        # Extract features and plot radar chart for Danceability, Energy, Valence, Acousticness
        song_features = {
            "danceability": song.get('danceability', 0),
            "energy": song.get('energy', 0),
            "valence": song.get('valence', 0),
            "acousticness": song.get('acousticness', 0)
        }
        
        # Plot radar chart (Note: You should add proper values to these fields)
        plot_radar_chart(song_features)

        # Recommend similar songs based on this song
        recommended_songs = recommend_songs(song['id'])
        if recommended_songs:
            st.subheader("Recommended Songs:")
            for rec_song in recommended_songs:
                st.write(f"- {rec_song['name']} by {rec_song['artists'][0]['name']}")
                st.image(rec_song['album']['images'][0]['url'], width=100)
        else:
            st.write("No similar songs found.")
    else:
        st.write("Song not found.")










