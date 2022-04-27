from operator import ge
from shutil import move
import pandas as pd
import numpy as np
# for closed match movies
import difflib
# for convert text to numerical feature vector
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies_data = pd.read_csv('/Users/deepakverma/Desktop/DataScience/movie_app/movies.csv', index_col = 'index')

# print(movies_data.head())

selected_features = ['genres','keywords','tagline','vote_average','cast','director','overview']

#replacing null values with null string
for feature in selected_features:
  movies_data[feature]=movies_data[feature].fillna('')

# print(movies_data[selected_features].info())

combined_features = movies_data['genres']+movies_data['keywords']+movies_data['tagline']+movies_data['cast']+movies_data['director']+movies_data['overview']
features=pd.DataFrame(combined_features)
features.columns=['text']

#combining text data to feature vectors
vectorizer = TfidfVectorizer()
# can use Series 'combined_features' as well
feature_vector = vectorizer.fit_transform(features['text'])
# print(feature_vector)

similarity = cosine_similarity(feature_vector)
# print(similarity)

#movie name list present in our Dataset
list_of_all_titles = movies_data['title'].tolist()
# print(list_of_all_titles)

def collabRecommendation(movie_name, total):
  try:
    #movie name list present in our Dataset
    find_close_match = difflib.get_close_matches(movie_name,list_of_all_titles)
    close_match = find_close_match[0]

    # finding index of close_match in movies_data
    index = movies_data[movies_data.title==close_match].index.values[0]

    df1= pd.DataFrame(similarity[index], columns=['similarity']) #DataFrame
    df2 = pd.DataFrame(movies_data.title) #DataFrame
    df = pd.concat([df1 , df2], axis=1)

    # sorting movies based on similarity score with close_match
    df = df.sort_values(by=['similarity'], ascending=False)

    # printing name of the similar movies using index from the similarity score
    print('top ', total, ' movies suggested for you are : ')
    df = pd.DataFrame(df.title[:total])
    df.rename(columns = {'title':'Movie Name'}, inplace = True)
    df.reset_index(drop=True, inplace=True)
    df.index = df.index+1
    # print(df.movieName.to_string(index=False))
    return df
  except:
    print("atleast enter 1 recommendation")
 
#user movie name and recommendation req input
# movie_name = input('enter your fav movie name : ')
# total = int(input('recommendations req : '))
# movie_name, total = "iron man", 5
# print(collabRecommendation(movie_name, total))

def bestRatingNMovies(total):
  try:
    movieN = movies_data[['title','vote_average']]
    # Sorting by column 'vote_average' descending
    movieN = movieN.sort_values(by=['vote_average'], ascending=False)
    movieN = movieN[:total]
    # movieN = pd.DataFrame(movieN['title'])
    movieN.rename(columns = {'title':'Movie Name','vote_average':'user ratings'}, inplace = True)
    movieN.reset_index(drop=True, inplace=True)
    movieN.index = movieN.index+1
    # print('top ', total, ' movies suggested for you are : ')
    # print(movieN.to_string(index=False))
    return movieN
  except:
    print("atleast enter 1 recommendation")
    
#user choice for N most rated movies
# suggest_req = int(input('number of top rated movie recommendations req : '))
# bestRatingNMovies(suggest_req)

def genreBestNMovies(genre_req,total):
  try:
    # total = 7
    genre_req = genre_req.lower()
    movieN = movies_data[['genres','title','vote_average']]
    # Filter data table with genres using query
    movieN = movieN[movieN['genres'].str.lower().str.contains(genre_req)]
    # Sorting by column 'vote_average' descending
    movieN = movieN.sort_values(by=['vote_average'], ascending=False)
    movieN = movieN[:total]
    # movieN = pd.DataFrame(movieN['title'])
    movieN = movieN[['title','vote_average']]
    movieN.rename(columns = {'title':'Movie Name','vote_average':'User Ratings'}, inplace = True)
    movieN.reset_index(drop=True, inplace=True)
    movieN.index = movieN.index+1
    print(movieN)
    # print('top ', total, ' movies suggested for you are : ')
    # print(movieN.to_string(index=False))
    return movieN
  except:
    print("atleast enter 1 recommendation")
    
#user choice for N most rated movies
# genre_req = input('enter your fav movie name : ')
# total = int(input('number of top rated movie recommendations req : '))
genre_req , total = 'Action',9
genreBestNMovies(genre_req,total)
