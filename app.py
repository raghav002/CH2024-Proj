from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load data
courses_df = pd.read_csv("courses.csv")  # Columns: title, description, credits, prerequisites
requirements_df = pd.read_csv("degree_requirements.csv")  # Columns: Category, Subcategory, Courses, Number needed

def recommend_courses(interests, courses_df):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(courses_df['description'])
    user_vector = vectorizer.transform([interests])
    similarity_scores = cosine_similarity(user_vector, tfidf_matrix).flatten()
    courses_df['similarity'] = similarity_scores
    return courses_df.sort_values(by='similarity', ascending=False)

def generate_schedule(user_data):
    max_credits = user_data['credits_per_semester']
    transfer_credits = user_data['transfer_credits']
    completed_courses = user_data['completed_courses']
    interests = user_data['interests']
    
    # Filter courses based on interests
    recommended_courses = recommend_courses(interests, courses_df)
    
    # Create a schedule
    schedule = []
    remaining_requirements = requirements_df.copy()
    total_credits = transfer_credits
    
    for semester in range(1, 9):  # Up to 8 semesters
        semester_credits = 0
        semester_courses = []
        
        for _, course in recommended_courses.iterrows():
            if semester_credits + course['credits'] > max_credits:
                break
            if course['title'] in completed_courses:
                continue
            prerequisites = course['prerequisites'].split(',') if course['prerequisites'] else []
            if all(prereq in completed_courses for prereq in prerequisites):
                semester_courses.append(course['title'])
                semester_credits += course['credits']
                completed_courses.append(course['title'])
                total_credits += course['credits']
                
                # Update remaining requirements
                for _, req in remaining_requirements.iterrows():
                    if course['title'] in req['Courses']:
                        req['Number needed'] -= 1
        
        schedule.append({'Semester': semester, 'Courses': semester_courses, 'Credits': semester_credits})
        if total_credits >= 120:  # Stop if degree requirements are met
            break
    
    return schedule

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_schedule', methods=['POST'])
def generate_schedule_endpoint():
    user_data = request.json
    schedule = generate_schedule(user_data)
    return jsonify(schedule)

if __name__ == '__main__':
    app.run(debug=True)
