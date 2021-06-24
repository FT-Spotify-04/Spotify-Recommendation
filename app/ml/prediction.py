import pandas as pd
import joblib
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates


# Instatiate the router
router = APIRouter()

# Instantiate templates
templates = Jinja2Templates(directory="app/templates/")

# Load tables and model
spotify = pd.read_csv('app/data/trimmed_spotify.csv')
dtm = pd.read_csv('app/data/dtm.csv')
nn = joblib.load('app/ml/nlp_model')

def song_recommend(track, artist):
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

    # Instantiate song list
    song_list = []
    for i in neigh_index[0][1:]:
        song_list.append(f"{spotify['track_name'][i]} by {spotify['track_artist'][i]}")
    return song_list

# track = 'Juke Box Hero'
# artist = 'Foreigner'
# print(song_recommend(artist, track))

@router.post('/prediction')
def echo(
    request: Request,
    name: str=Form(...),
    artist: str=Form(...)
        ):
    """Gets the input data from index.html (with respective dtypes
    included) and passes them into the predict function (used as a
    helper function).
    """

    # Make the prediction
    # prediction = song_recommend(name,artist)
    prediction = name

    return templates.TemplateResponse('prediction.html',
                                      {"request": request,
                                       "prediction": prediction
                                       })

# Route for display of the prediction page
@router.get('/prediction')
def display_index(request: Request):
    return templates.TemplateResponse('prediction.html', {"request": request})