import streamlit as st
import pickle
import pandas as pd
import requests
from PIL import Image
movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
similarity=pickle.load(open('similarity.pkl','rb'))

def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=66de26666afe6e2669c627789a84fbc6&language=en-US'.format(movie_id))
    data = response.json()
    if(data.get('poster_path') == None):
        return Image.open('poster.png')
    return "https://image.tmdb.org/t/p/original/"+data['poster_path']

def recommend(movie_name):
    movie_idx=movies[movies['title']==movie_name].index[0]
    distances=similarity[movie_idx]
    movies_list=sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:26]
    result=[]
    posters=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].id
        result.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))
    return result,posters

def display_poster(names, posters):
    for i in range(0, len(names), 5):
        with st.container():
            cols = st.columns(5)
            for j in range(0, 5):
                if(i+j < len(names)):
                    with cols[j]:
                        st.text(names[i+j])
                        st.image(posters[i+j])

st.title('Movie Recommender System') 

selected_movie_name = st.selectbox(
    'Select movie you have watched ',
    movies['title'].values)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
    display_poster(names,posters)