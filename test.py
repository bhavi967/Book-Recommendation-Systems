#import the libraries 
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

st.header("Book Recommender System")

st.markdown('''
           #### The site using collaborative filtering suggests books             from our catlog.
           #### We recommend top 50 books for every one as well
           ''')

#import our models:
import pickle
popular = pickle.load(open('pop.pkl','rb')) 
books= pickle.load(open('books.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))


#Top 50 Books

st.sidebar.title('Top 50 Books')

if st.sidebar.button("SHOW"):
    cols_per_row= 5
    num_rows = 10
    for row in range(num_rows):
        cols= st.columns(cols_per_row)
        for col in range(cols_per_row):
            book_idx = row+cols_per_row + col 
            if book_idx < len(popular):
                with cols[col]:
                    st.image(popular.iloc[book_idx]['Image-URL-M'])
                    st.text(popular.iloc[book_idx]['Book-Title'])
                    st.text(popular.iloc[book_idx]['Book-Author'])

#function to recommend

def recommend(book_name):
    index = np.where(pt.index == book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse= True)[1:6]
    #lets create empty list that lies I want to populate with the book information
    #book author book-titke image url 
    data=[]
    for i in similar_items:
        item=[]
        temp_df = books[books['Book-Title']== pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)
    return data                  

book_list = pt.index.values

st.sidebar.title("Similar Book Recommendations")
selected_book =st.sidebar.selectbox("Select a book from the dropdown",book_list)
if st.sidebar.button("Recommend Me"):
    book_recommend = recommend(selected_book)
    cols = st.columns(5)
    for col_idx in range(5):
         with cols[col_idx]:
              if col_idx < len(book_recommend):
                  st.image(book_recommend[col_idx][2])
                  st.text(book_recommend[col_idx][0])
                  st.text(book_recommend[col_idx][1])

#import data

books = pd.read_csv(r'C:\Users\karna\Downloads\rec_data\Books.csv')
users = pd.read_csv(r'C:\Users\karna\Downloads\rec_data\Users.csv')
ratings = pd.read_csv(r'C:\Users\karna\Downloads\rec_data\Ratings.csv')

st.sidebar.title("Data Used")

if st.sidebar.button("Show"):
    st.subheader("This is the books data that we used in the model")
    st.dataframe(books)
    st.subheader("This is the books user ratings that we used in the model")
    st.dataframe(ratings)
    st.subheader("This is the user data that we used in the model")
    st.dataframe(users)