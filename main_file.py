import streamlit as st
import pandas as pd
import numpy as num
from PIL import Image
import base64
import streamlit as st
import sklearn
import requests
from bs4 import BeautifulSoup
import pickle
import fastparquet
import dask.dataframe as dd


# import data

url_links = "https://drive.google.com/file/d/1qoSPNulwSEgl-7hU0h6n2pq-ajfvysyS/view?usp=sharing"
path_links = 'https://drive.google.com/uc?export=download&id='+url_links.split('/')[-2]
links = pd.read_csv(path_links)


url_movies = "https://drive.google.com/file/d/1_I8qM82wyV-ly5DKfVHvkAx5DItQSyeY/view?usp=sharing"
path_movies = 'https://drive.google.com/uc?export=download&id='+url_movies.split('/')[-2]
movies = pd.read_csv(path_movies)


url_ratings = "https://drive.google.com/file/d/1wl7iibcSBR6WgsywPAX49rQTWsHscmg7/view?usp=sharing"
path_ratings = 'https://drive.google.com/uc?export=download&id='+url_ratings.split('/')[-2]
ratings = pd.read_csv(path_ratings)


url_tags = "https://drive.google.com/file/d/1tFgO1Fm3MUxiLl_yWzWMx4a0Tw-u_1dD/view?usp=sharing"
path_tags = 'https://drive.google.com/uc?export=download&id='+url_tags.split('/')[-2]
tags = pd.read_csv(path_tags)



# predictions: Read Parquet file using Dask

p_dd = dd.read_parquet('predictions.parquet')


# SETTINGS:
# number of recommendations n
n=5
# number of shown recommenation columns 
num_columns = 5


# pub recommendations imdb pics
def extract_image_url(imdb_id):
    # First, try with the IMDb URL having "/tt00" in the link
    html_url = f"https://www.imdb.com/title/tt00{imdb_id}/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    
    # Send an HTTP GET request to fetch the HTML content
    response = requests.get(html_url, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the <meta> tag with the property "og:image"
        meta_tag = soup.find("meta", {"property": "og:image"})

        if meta_tag:
            pic_url = meta_tag["content"]
            return pic_url
        else:
            return "Image URL not found on the page"
            
    elif response.status_code == 404:
        # If the page is not found (404), try with the IMDb URL having "/tt0" in the link
        html_url = f"https://www.imdb.com/title/tt0{imdb_id}/"
        response = requests.get(html_url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            meta_tag = soup.find("meta", {"property": "og:image"})

            if meta_tag:
                pic_url = meta_tag["content"]
                return pic_url
            else:
                return "Image URL not found on the page"

    elif response.status_code == 404:
        # If the page is not found (404), try with the IMDb URL having "/tt0" in the link
        html_url = f"https://www.imdb.com/title/tt{imdb_id}/"
        response = requests.get(html_url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            meta_tag = soup.find("meta", {"property": "og:image"})

            if meta_tag:
                pic_url = meta_tag["content"]
                return pic_url
            else:
                return "Image URL not found on the page"


        else:
            return f"Fai1. Status code: {response.status_code}"
    else:
        return f"Fail2. Status code"

    
    

# SURPRISE DATA
def get_top_n_for_user(p_dd, user_id, n=5):
    iids = []
    p = p_dd.loc[p_dd["uid"]==user_id,:].compute().sort_values(by="est", ascending=False)[0:n]
    iids = p["iid"].values.tolist()
    top_n_df = pd.merge(links.loc[links["movieId"].isin(iids),:], 
        movies,
        how="left",
        on="movieId")

    return top_n_df







st.title(":star: Best movie rating for YOU :star:") 
st.write(""" The popular movies """)



st.markdown("---")

import streamlit as st
from PIL import Image
from itertools import cycle

filteredImages =  ['Unknown.jpeg', 'fight.jpg', 'pulpfiction.jpg', 'LEON - French Poster by Laurent Lufroy.jpeg', '71Ke3uo-vjL._SL1500_.jpg', '918-iKMNQ3L._SL1500_.jpg', '20120704-191812.jpg.webp', 'pitch_perfect-419842614-large.jpg'] # your images here
caption = ['[ID-7361] Eternal Sunshine of the Spotless Mind (2004)', '[ID-2959] Fight Club (1999)', '[ID-296] Pulp Fiction (1994)', '[ID-293] Léon: The Professional(1994)', '[ID-84847] Emma (2009)', '[ID-96588] Toy Story 2 (1999)', '[ID-858] Godfather, The (1972)', '[ID-3114] Pitch Perfect (2012)' ] # your caption here
cols = cycle(st.columns(4)) # st.columns here since it is out of beta at the time I'm writing this
for idx, filteredImage in enumerate(filteredImages):
    next(cols).image(filteredImage, width=150, caption=caption[idx])


st.markdown("---")
    

st.title("Let's guess the best movie you've NEVER seen") 
NumMov = st.number_input("Chose the ID of your favourite movie from the pictures above", min_value=1, max_value=193609, value=858, step=1) #st.text_input("Log In with User ID:")

st.write("Which one do you chose for today's evening ?")




#ITEM BASED

#result_2 = pd.read_csv("./movie_data.csv")

url = "https://drive.google.com/file/d/1zNoEHDvb2eHfAoFIyFY05WMqcVQTW14o/view?usp=sharing"
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
result_2 = pd.read_csv(path)



list_of_ids = (7361, 2959, 172, 296, 293,1730, 50, 96588, 4104, 84847, 413, 27831, 3114, 858)
rrr = result_2[result_2['movieId'].isin(list_of_ids)].drop_duplicates(subset='title')  
new = rrr[['movieId', 'userId', 'rating']]
user_movie_matrix = pd.pivot_table(data=new,
                                  values='rating',
                                  index='userId',
                                  columns='movieId',
                                  fill_value=0)
movie_correlations_matrix = user_movie_matrix.corr()
blonde_correlations_df = pd.DataFrame(movie_correlations_matrix[NumMov])
blonde_correlations_df = blonde_correlations_df[blonde_correlations_df.index != NumMov]
blonde_correlations_df = blonde_correlations_df.sort_values(by=NumMov, ascending=False) 

blonde_top_10_correlation = (blonde_correlations_df
                                  .head(3)
                                  .reset_index()
                                  .merge(rrr.drop_duplicates(subset='movieId'),   #subset by which column we will drop the duplicates
                                         on='movieId',
                                         how='left')
                                  [['title']]      #'movieId',
                            )   #names of columsns we will have
blonde_top_10_correlation




### USER-BASED RECOMMENDER
st.write("### This movie as that was needed to spend an UNFORGETTABLE evening:")

userId = st.text_input("Log In with User ID:")

if userId:
    top_n = get_top_n_for_user(p_dd, int(userId), n)
    for i in range(num_columns):
        imdb=top_n.loc[i, "imdbId"]
        if i % num_columns == 0:
            col0, col1, col2, col3, col4 = st.columns(5)
    
        #pic_path = f"C:/Users/daedlow/Documents/jupyter_notebook/recommender_systems/pic_db/{imdb}_pic.csv"

        pic_url = extract_image_url(imdb)
         

        with locals()[f"col{i % num_columns}"]:
            st.write(top_n.loc[i, "title"])
            if pic_url:
                st.image(pic_url)
            if pic_url is None:
                st.write("no picture available")

st.markdown("---")


image = Image.open('Why-is-Popcorn-a-Movie-Food.jpg')
st.image(image, caption='Have a nice watching')

















































#int_val = st.number_input('Seconds', min_value=1, max_value=10, value=5, step=1)


#import pandas as pd
#import streamlit as st

#data_df = pd.DataFrame(
 #   {
  #      "apps": [
   #         "https://drive.google.com/file/d/1YWv5C1QGxdBx3_aZbncxFdEtQG1Wu9ob/view?usp=sharing",
  #      ],
 #   }
#)

#st.data_editor(
#    data_df,
#    column_config={
#        "apps": st.column_config.ImageColumn(
#            "Preview Image", help="Streamlit app preview screenshots"
#        )
#    },
#    hide_index=True,
#)









#from PIL import Image

#image = Image.open('images.jpeg')
#image_2 = Image.open('Unknown.jpeg')
#st.image(image, caption='Sunrise by the mountains')
#st.image(image_2, caption='Sunrise by the mountainsssss')

#st.write("The price of the house is:", prediction)

#st.write('Hello')
#st.baloon()