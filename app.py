import streamlit as st
import pandas as pd
import pickle
import requests

st.title('Movie Recommendation System')
mov = pd.read_pickle("./dummy.pkl")

similarity = pickle.load(open('similarity.pkl', 'rb'))


def get_posters(mov_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(mov_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']


def recommend(movie):
    curr = mov[mov['title'] == movie].index[0]
    names = []
    posters = []
    for x, y in sorted(list(enumerate(similarity[curr])) , reverse = True , key = lambda x : x[1])[1:6]:
        currmov = mov.iloc[x]
        names.append(currmov['title'])
        posters.append(get_posters(currmov['id']))
    return names, posters


option = st.selectbox(
    'Select a movie:',
    mov['title'].values)

if st.button('Recommend:'):
    names, posters = recommend(option)

    ncol = len(names) # (which is the number trues in a dataframe column)
    # wcol = 5

    cols = st.columns(ncol)

    for i in range(ncol):
        # col = cols[i % wcol]
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
