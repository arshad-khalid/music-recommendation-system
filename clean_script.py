import pandas as pd

# Load the dataset
file_path = 'music.csv'  # Replace with your actual file path
data = pd.read_csv(file_path)

# Step 1: Clean 'artists' field (remove string formatting from lists)
data['artists'] = data['artists'].str.replace("[", "").str.replace("]", "").str.replace("'", "")
print(data['artists'][8])
data.info()

# Step 2: Delete 'release_date' column
del data['release_date']

# Step 3: Filter out outliers
# Remove rows where 'duration_ms' is less than 30 seconds or more than 30 minutes
data_cleaned = data[(data['duration_ms'] >= 30000) & (data['duration_ms'] <= 1800000)]

# Remove rows where 'tempo' is zero or negative (since tempo cannot be zero in real-world cases)
data_cleaned = data_cleaned[data_cleaned['tempo'] > 0]

# Step 4: Round off the numbers in the necessary columns
data_cleaned['valence'] = data_cleaned['valence'].round(4)
data_cleaned['acousticness'] = data_cleaned['acousticness'].round(3)
data_cleaned['danceability'] = data_cleaned['danceability'].round(3)
data_cleaned['energy'] = data_cleaned['energy'].round(3)
data_cleaned['instrumentalness'] = data_cleaned['instrumentalness'].round(4)
data_cleaned['liveness'] = data_cleaned['liveness'].round(3)
data_cleaned['loudness'] = data_cleaned['loudness'].round(3)
data_cleaned['speechiness'] = data_cleaned['speechiness'].round(4)
data_cleaned['tempo'] = data_cleaned['tempo'].round(3)

# Step 5: Check if the cleaned dataset is smaller (confirming the filters worked)
print(f"Original dataset size: {len(data)}")
print(f"Cleaned dataset size: {len(data_cleaned)}")

# Step 6: Save the cleaned dataset to a new CSV file
output_path = 'cleaned_music.csv'
data_cleaned.to_csv(output_path, index=False)

print(f"Cleaned data saved to {output_path}")