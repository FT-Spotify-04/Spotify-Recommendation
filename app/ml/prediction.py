import pandas as pd
import joblib

spotify = pd.read_csv(r'app\data\trimmed_spotify.gz')
dtm = pd.read_csv(r'app\data\dtm.csv')

nn = joblib.load(r'app\ml\nlp_model')

def song_recommend(artist, track):
    """
    Will take the user input and return back a list of songs
    that is like the song that user put
    """
    # Gets the song index from the spotify dataframe.
    selected_index = spotify[(spotify['track_name']==track) & (spotify['track_artist']==artist)].index.tolist()
    # Gets the row that has the song index from the vectorized dataframe
    selected_song = [dtm.iloc[selected_index[0]].values]
    # Running the row through the loaded model
    _, neigh_index = nn.kneighbors(selected_song)
    song_list = []
    for i in neigh_index[0][1:]:
        song_list.append(f"{spotify['track_name'][i]} by {spotify['track_artist'][i]}")
    return song_list

track = 'Juke Box Hero'
artist = 'Foreigner'
print(song_recommend(artist, track))