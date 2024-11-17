from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from app.database import get_connection

def recommend_courses(user_interests, top_n=5):
    conn = get_connection()
    courses_df = pd.read_sql_query("SELECT * FROM courses", conn)
    conn.close()

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(courses_df['description'])

    user_vector = vectorizer.transform([user_interests])
    similarities = cosine_similarity(user_vector, tfidf_matrix).flatten()

    courses_df['similarity'] = similarities
    return courses_df.sort_values(by='similarity', ascending=False).head(top_n)
