import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from requests.exceptions import HTTPError
import time 

# Spotify API Setup
client_id = "8c662d4fe4f049c9a479cc16d2f05e76"
client_secret = "d4450a692f7f4263888dc66f21cf8d43"

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Function to fetch song details
def find_song(song_name):
    """Searches for a song on Spotify and returns its details."""
    result = sp.search(q=song_name, limit=1, type='track')
    if result['tracks']['items']:
        return result['tracks']['items'][0]
    return None

# Function to get similar songs based on a song
def recommend_songs(song_id):
    """Recommends similar songs based on a given song ID."""
    results = sp.recommendations(seed_tracks=[song_id], limit=5)
    return results['tracks']

# # Function to fetch song lyrics (using a third-party API)
def get_lyrics(song_name, artist_name):
    """Fetch lyrics for a given song from a lyrics API."""
    try:
        response = requests.get(f"https://api.lyrics.ovh/v1/{artist_name}/{song_name}")
        response.raise_for_status()
        return response.json().get("lyrics", "Lyrics not found.")
    except HTTPError:
        return "Error fetching lyrics."
time.sleep(1)
# Function to plot radar chart for song features
def plot_radar_chart(features):
    """Plot radar chart for song features like danceability, energy, etc."""
    categories = ['Danceability', 'Energy', 'Valence', 'Acousticness', 'Speechiness']
    values = [features.get(category.lower(), 0) for category in categories]
    
    # Radar chart setup
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='b', alpha=0.25)
    ax.plot(angles, values, color='b', linewidth=2)

    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)

    st.pyplot(fig)
time.sleep(1)
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
        
        st.image(song['album']['images'][0]['url'], width=300)
        
        # Display song audio features
        features = sp.audio_features(song['id'])[0]
        st.write("**Audio Features:**")
        st.write(f" - Danceability: {features['danceability']}")
        st.write(f" - Energy: {features['energy']}")
        st.write(f" - Valence: {features['valence']}")
        st.write(f" - Acousticness: {features['acousticness']}")
        st.write(f" - Speechiness: {features['speechiness']}")

        # Plot radar chart for audio features
        plot_radar_chart(features)

        # Get lyrics for the song
        lyrics = get_lyrics(song['name'], song['artists'][0]['name'])
        st.subheader("Lyrics:")
        st.write(lyrics)

        # Recommend similar songs
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
