from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load data
def load_data():
    courses = pd.read_csv('data/cs_courses.csv')
    requirements = pd.read_csv('data/cs_requirements.csv')
    return courses, requirements

courses, requirements = load_data()

# Recommendation function
def recommend_courses(interests, courses, requirements, top_n=5):
    # Combine user interests with course descriptions for similarity matching
    vectorizer = TfidfVectorizer(stop_words='english')
    course_descriptions = courses['description'].fillna('')
    tfidf_matrix = vectorizer.fit_transform(course_descriptions)

    # Transform user interests into the same TF-IDF space
    interest_vector = vectorizer.transform([interests])

    # Compute cosine similarity
    similarity_scores = cosine_similarity(interest_vector, tfidf_matrix).flatten()

    # Filter courses by requirements
    filtered_courses = pd.DataFrame()
    for _, row in requirements.iterrows():
        required_list = row['Courses'].split(',')
        num_needed = int(row['Number of Courses'])
        subcategory_courses = courses[courses['title'].isin(required_list)]
        
        # Sort by similarity and take the top 'num_needed' courses
        subcategory_indices = subcategory_courses.index
        subcategory_scores = similarity_scores[subcategory_indices]
        top_subcategory_indices = subcategory_indices[subcategory_scores.argsort()[-num_needed:][::-1]]
        filtered_courses = pd.concat([filtered_courses, courses.loc[top_subcategory_indices]])

    # Rank all filtered courses by similarity
    filtered_scores = similarity_scores[filtered_courses.index]
    top_indices = filtered_scores.argsort()[-top_n:][::-1]
    recommended_courses = filtered_courses.iloc[top_indices]

    return recommended_courses

# Routes
@app.route('/')
def home():
    return render_template('recommend.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_data = request.json
    interests = user_data.get('interests', '')
    num_recommendations = user_data.get('num_recommendations', 5)

    recommended_courses = recommend_courses(interests, courses, requirements, num_recommendations)
    response = recommended_courses[['title', 'description', 'Credits']].to_dict(orient='records')

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
