import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from fuzzywuzzy import process
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# Load your dataset
df = pd.read_csv('cleaned_music.csv')

# Select relevant features
features = ['valence', 'acousticness', 'danceability', 'energy', 'instrumentalness', 
            'liveness', 'loudness', 'speechiness', 'tempo']

# Standardize the features
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df[features])

# Fit a K-Nearest Neighbors model for recommendation
knn = NearestNeighbors(n_neighbors=10, metric='cosine', algorithm='brute')
knn.fit(df_scaled)

# Function to get the closest song name using fuzzy matching
def get_closest_song(song_name):
    song_list = df['name'].tolist()  # List of all song names
    closest_match = process.extractOne(song_name, song_list)  # Get the closest match
    return closest_match[0] if closest_match else None  # Return the best match if found

# Function to get songs by a specific artist
def get_songs_by_artist(artist_name):
    artist_list = df['artists'].tolist()  # List of all artists
    closest_artist = process.extractOne(artist_name, artist_list)  # Get the closest match
    if closest_artist is None:
        return None
    
    # Filter songs by the closest artist
    filtered_songs = df[df['artists'] == closest_artist[0]]
    return filtered_songs[['name', 'artists']]  # Return songs by the artist

# Function to get song recommendations based on a song name
def get_recommendations(song_name, n_recommendations=5):
    # Use fuzzy matching to find the closest song
    closest_song = get_closest_song(song_name)
    
    if closest_song is None:
        return f"No song found with a name close to: {song_name}"
    
    # Find the index of the closest song
    song_index = df[df['name'] == closest_song].index[0]
    
    # Find the nearest neighbors for the closest song
    distances, indices = knn.kneighbors([df_scaled[song_index]], n_neighbors=n_recommendations + 1)
    
    # Get the recommended song names along with their artists
    recommendations = df.iloc[indices[0][1:]]  # Skip the first one (itself)
    return recommendations[['name', 'artists']]  # Return a DataFrame with song names and artists

# GUI for the Music Recommendation System
class MusicRecommendationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Recommendation System")
        
        # Create the main frame
        self.frame = ttk.Frame(self.root, padding=10)
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Search Type Label and Combobox
        self.label = ttk.Label(self.frame, text="Search by:")
        self.label.grid(row=0, column=0, padx=5, pady=5)
        
        self.search_type = ttk.Combobox(self.frame, values=["Song", "Artist"], state="readonly")
        self.search_type.grid(row=0, column=1, padx=5, pady=5)
        
        # Input for song/artist name
        self.input_label = ttk.Label(self.frame, text="Enter Name:")
        self.input_label.grid(row=1, column=0, padx=5, pady=5)
        
        self.input_name = ttk.Entry(self.frame)
        self.input_name.grid(row=1, column=1, padx=5, pady=5)
        
        # Search Button
        self.search_button = ttk.Button(self.frame, text="Search", command=self.search)
        self.search_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        
        # Recommendations Listbox
        self.recommendations_label = ttk.Label(self.frame, text="Recommendations:")
        self.recommendations_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        
        self.recommendations_list = tk.Listbox(self.frame, width=50, height=10)
        self.recommendations_list.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def search(self):
        self.recommendations_list.delete(0, tk.END)  # Clear previous recommendations
        search_type = self.search_type.get()
        name = self.input_name.get()
        
        if search_type == "Song":
            recommendations = get_recommendations(name)
            if isinstance(recommendations, str):
                messagebox.showinfo("No Match Found", recommendations)
            else:
                for idx, (rec_song, rec_artist) in enumerate(zip(recommendations['name'], recommendations['artists']), 1):
                    self.recommendations_list.insert(tk.END, f"{rec_song} by {rec_artist}")
        
        elif search_type == "Artist":
            songs_by_artist = get_songs_by_artist(name)
            if songs_by_artist is None or songs_by_artist.empty:
                messagebox.showinfo("No Songs Found", f"No songs found for artist: {name}")
            else:
                song_list = [f"{idx+1}. {row['name']}" for idx, row in songs_by_artist.iterrows()]
                song_choice = simpledialog.askinteger("Select a Song", "Enter the song number for recommendations:\n" + "\n".join(song_list))
                
                if song_choice is not None and 0 < song_choice <= len(songs_by_artist):
                    selected_song = songs_by_artist.iloc[song_choice - 1]['name']
                    recommendations = get_recommendations(selected_song)
                    if isinstance(recommendations, str):
                        messagebox.showinfo("No Match Found", recommendations)
                    else:
                        for idx, (rec_song, rec_artist) in enumerate(zip(recommendations['name'], recommendations['artists']), 1):
                            self.recommendations_list.insert(tk.END, f"{rec_song} by {rec_artist}")
                else:
                    messagebox.showinfo("Invalid Selection", "Please select a valid song number.")

        else:
            messagebox.showinfo("Invalid Option", "Please select 'Song' or 'Artist'.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicRecommendationApp(root)
    root.mainloop()