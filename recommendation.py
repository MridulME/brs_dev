import pandas as pd
from model import recommend_books, book_df, tfidf_vectorizer, knn_model

def recommend_by_user_id(user_df, user_id):
    try:
        user_interest = user_df.loc[user_df['professor_id'] == user_id, 'interest_area'].values[0]
        recommendations = recommend_books(user_interest, book_df, tfidf_vectorizer, knn_model)
        if isinstance(recommendations, pd.DataFrame):
            return recommendations.to_dict(orient='records')
        else:
            return recommendations
    except IndexError:
        return f"No user found with ID {user_id}"
    except ValueError:
        return "Invalid user ID"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def recommend_by_interest_area(interest_area):
    try:
        recommendations = recommend_books(interest_area, book_df, tfidf_vectorizer, knn_model)
        if isinstance(recommendations, pd.DataFrame):
            return recommendations.to_dict(orient='records')
        else:
            return recommendations
    except Exception as e:
        return f"An unexpected error occurred: {e}"
