import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from database import get_data

# Connect to the database and get the data
book_df, user_df = get_data()

# Train the model
def train_model(book_df):
    try:
        all_titles = book_df['Title'].tolist()
        tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.8, min_df=3, ngram_range=(1, 2))
        tfidf_matrix = tfidf_vectorizer.fit_transform(all_titles)
        knn_model = NearestNeighbors(metric='cosine', algorithm='brute')
        knn_model.fit(tfidf_matrix)
        return tfidf_vectorizer, knn_model, tfidf_matrix
    except KeyError as e:
        return None, None, None
    except Exception as e:
        return None, None, None

tfidf_vectorizer, knn_model, tfidf_matrix = train_model(book_df)

# Recommend books
def recommend_books(interest_areas, book_df, tfidf_vectorizer, knn_model, top_n=5, similarity_threshold=0.1):
    try:
        interest_areas_list = [ia.strip() for ia in interest_areas.split(',')]
        interest_areas_tfidf = tfidf_vectorizer.transform(interest_areas_list)

        matching_books_indices = set()
        for interest_area_tfidf in interest_areas_tfidf:
            distances, indices = knn_model.kneighbors(interest_area_tfidf, n_neighbors=top_n)
            matching_indices = [indices[0][i] for i in range(len(distances[0])) if
                                distances[0][i] <= (1 - similarity_threshold)]
            matching_books_indices.update(matching_indices)

        if matching_books_indices:
            recommended_books = book_df.iloc[list(matching_books_indices)]
            return recommended_books
        else:
            return "No matching books found"
    except Exception as e:
        return "No matching books found due to an error."
