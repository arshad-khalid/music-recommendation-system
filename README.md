# 🎵 Music Recommendation System

**Music Recommendation System**, a project for discovering new music based on user input. This system uses a dataset of songs (CSV) obtained from kaggle to recommend tracks that match your input, utilizing advanced machine learning techniques to provide personalized suggestions.

## Overview

The Music Recommendation System is built using Python and leverages several powerful libraries:

- **Pandas**: For data manipulation and analysis, allowing easy handling of the dataset.
- **Scikit-learn**: Used for machine learning algorithms, particularly the **K-Nearest Neighbors (KNN)** algorithm, which identifies similar songs based on audio features.
- **FuzzyWuzzy**: For fuzzy string matching, helping to find song or artist names even if they are not an exact match.
- **Tkinter**: A standard GUI toolkit for creating the user interface, making it easy to interact with the system.

The dataset used, `music.csv`, contains a variety of songs with different audio features but lacks genre information. The system processes this data to provide recommendations based solely on the audio characteristics of the songs.

## Recommendation Calculation

The recommendation process in the Music Recommendation System primarily falls under the domain of **Content-Based Filtering**. This method relies on the attributes of the items being recommended—in this case, the songs—rather than user behavior or preferences. Here’s a detailed breakdown of how the recommendation is calculated:

1. **Feature Extraction**: Each song in the dataset is represented by a set of numerical features derived from its audio characteristics. Key features used in this system include:
   - **Acousticness**: Measures the degree to which a track is acoustic.
   - **Danceability**: Describes how suitable a track is for dancing based on tempo, rhythm stability, and overall regularity.
   - **Energy**: Represents the intensity and activity of a track.
   - **Instrumentalness**: Predicts whether a track contains no vocals.
   - **Liveness**: Indicates the presence of an audience in the recording.
   - **Loudness**: The overall loudness of a track in decibels (dB).
   - **Speechiness**: A measure of the presence of spoken words in a track.
   - **Tempo**: The speed of the music, measured in beats per minute (BPM).
   - **Valence**: A measure of the musical positiveness conveyed by a track.

2. **Data Normalization**: Before recommendations are generated, the audio feature data is normalized using `StandardScaler`. This process standardizes the feature values to ensure that all features contribute equally to distance calculations, which is crucial for the accuracy of the K-Nearest Neighbors (KNN) algorithm.

3. **Distance Calculation**: The KNN algorithm calculates the similarity between the user's input song (or artist) and all other songs in the dataset based on their audio features. The similarity is typically measured using the **Euclidean distance** formula, which determines how far apart the songs are in the multi-dimensional feature space.

4. **Finding Nearest Neighbors**: Once the distances are calculated, the algorithm identifies the **k-nearest neighbors** to the input song. The user can specify the number of recommendations they want (e.g., 5), and the system retrieves the closest songs based on their feature similarities.

5. **Recommendation Output**: The system presents the identified nearest songs as recommendations to the user. These recommendations are expected to share similar audio characteristics with the input song, providing the user with a personalized list of new music to explore.

## Limitations

- **Lack of Genre Information**: The system does not use genres to make recommendations. Instead, it relies solely on audio features, which may limit the diversity of recommendations for users who prefer specific genres.
- **Feature Dependence**: The quality of recommendations heavily depends on the accuracy and comprehensiveness of the audio features available in the dataset. Missing or inaccurate features may lead to less relevant recommendations.

## Future Updates

To enhance the Music Recommendation System, future updates could include:

- **Incorporating Genre Information**: If genre data becomes available, it could be integrated to refine recommendations further and cater to users' specific musical preferences.
- **User Preference Learning**: Implementing user feedback mechanisms to learn from users' choices over time, thereby improving the personalization of recommendations.
- **Enhanced UI/UX**: Improving the user interface to make it more engaging and user-friendly, potentially integrating additional features like user playlists or sharing options.
