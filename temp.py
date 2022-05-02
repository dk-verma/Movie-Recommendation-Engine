#importing dependencies
# from matplotlib.pyplot import close
import pandas as pd
# import numpy as np
import difflib
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#reading data from csv files
df1 = pd.read_csv("./tmdb_5000_credits.csv")
# df = pd.read_csv("./tmdb_5000_movies.csv")
df = pd.read_csv("./5000_movies.csv")


df1.columns = ['id','title','cast','crew']
# df1.info()
# df.info()

df=df[['id','title','genres','keywords','original_language','vote_average','vote_count']]
# df.info()

# merging given 2 DataFrames
df = df.merge(df1, on=["id","title"])
df.original_language.unique()
df = df[(df.original_language=='en') & (df.vote_count>100) | (df.original_language=='hi')]
# df.info()

features = ["cast", "crew", "keywords", "genres"]
for feature in features:
    df[feature] = df[feature].apply(literal_eval)
# df[features].head()

def get_director(x):
    for i in x:
        if i["job"] == "Director":
            return i["name"]
    return ""
    # return np.nan
    

def get_list(x):
    name_list = []
    if isinstance(x, list):
        name_list = [ obj["name"] for obj in x ]
        # if len(name_list) > 3:
        name_list = name_list[:3]
    return name_list

df["director"] = df["crew"].apply(get_director)

features = ["cast", "keywords", "genres"]
for feature in features:
    df[feature] = df[feature].apply(get_list)

# The next step would be to convert the above feature instances into lowercase a nd remove all the spaces between them

def clean_data(row):
    if isinstance(row, list):
        return [str.lower(i.replace(" ", "")) for i in row]
    else:
        if isinstance(row, str):
            return str.lower(row.replace(" ", ""))
        else:
            return ""
features = ['cast', 'keywords', 'director', 'genres']

for feature in features:
    df[feature] = df[feature].apply(clean_data)

# Now, let’s create a “text” containing all of the metadata information extracted to input into the vectorizer

def create_soup(features):
    return ' '.join(features['genres']) + ' ' + ' '.join(features['cast']) + ' ' + features['director'] + ' ' + ' '.join(features['keywords'])

df["text"] = df.apply(create_soup, axis=1)
# print(df["text"].head())

# df.drop(['crew','vote_count','original_language'],axis=1,inplace=True)
df.reset_index(drop=True, inplace=True)
df.index = range(df.shape[0])
# df[-5:]

count_vectorizer = TfidfVectorizer(stop_words="english")
count_matrix = count_vectorizer.fit_transform(df["text"])
similarity = cosine_similarity(count_matrix, count_matrix) 

list_of_all_titles = df['title'].tolist()

def contentRecommendation(title, total):
    df2=pd.DataFrame(['Movie not in Database'],columns =['Movie Name'])
    try:
        title=title.lower()
        # finding index of close_match in movies_data
        find_close_match = difflib.get_close_matches(title,list_of_all_titles)
        close_match = find_close_match[0]
        # print(close_match)
        idx = df[df.title==close_match].index.values[0]
        df1 = pd.DataFrame(similarity[idx], columns=['similarity']) #DataFrame
        df2 = pd.DataFrame(df.title) #DataFrame
        df2 = df1.join(df2)
        # df2 = pd.concat([df1,df2], axis=1)
        df2 = df2.sort_values(by=['similarity'], ascending=False)
        # printing name of the similar movies using index from the similarity score
        print('top ', total, ' movies suggested for you are ')
        df2 = pd.DataFrame(df2.title[:total])
        df2.rename(columns = {'title':'Movie Name'}, inplace = True)
        df2.reset_index(drop=True, inplace=True)
        df2.index = df2.index+1
        # print(df.movieName.to_string(index=False))
        return df2
    except:
        # print("atleast enter 1 recommendation")
        return df2
        
# print("################ Content Based System #############")
# total=8
# print(contentRecommendation("Matrix", total))

def bestRatingNMovies(total):
    try:
        # movieN = movies_data[['title','vote_average']]
        movieN = df[['title','vote_average']]
        # Sorting by column 'vote_average' descending
        movieN = movieN.sort_values(by=['vote_average'], ascending=False)
        movieN = movieN[:total]
        movieN.rename(columns = {'title':'Movie Name','vote_average':'IMDB Ratings'}, inplace = True)
        movieN.reset_index(drop=True, inplace=True)
        movieN.index = movieN.index+1
        # print('top ', total, ' movies suggested for you are : ')
        # print(movieN)
        # print(movieN.to_string(index=False))
        return movieN
    except:
        print("atleast enter 1 recommendation")
    
# print("################ Rating Based System #############")    
# suggest_req=10
# print(bestRatingNMovies(suggest_req))

# print(df.genres)

def genreBestNMovies(genre_req,total):
    try:
        genre_req = genre_req.lower()
        movieN = df[['genres','title','vote_average']]
        # Sorting by column 'vote_average' descending
        movieN = movieN.sort_values(by=['vote_average'], ascending=False)
        # Filter data table with genres using query
        ans=[]
        count,i=0,0,
        while count<total:
            if genre_req in movieN.genres.iloc[i]:
                ans.append(movieN[['title','vote_average']].iloc[i])
                count+=1
            i+=1
        ans = pd.DataFrame(ans)
        ans.columns=['Movie Name','IMDB Ratings']
        # movieN = pd.DataFrame(movieN['title'])
        ans.reset_index(drop=True, inplace=True)
        ans.index = ans.index+1
        # print(ans)
        return ans
    except:
        print("atleast enter 1 recommendation")   

# print("################ Genre Based System #############")
# genre_req , total = 'action', 8
# print(genreBestNMovies(genre_req,total))
