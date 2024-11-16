from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load data
courses_df = pd.read_csv("courses.csv")  # Columns: title, description, credits, prerequisites
requirements_df = pd.read_csv("degree_requirements.csv")  # Columns: Category, Subcategory, Courses, Number needed

# Helper function: Check prerequisites
def check_prerequisites(prerequisite_string, completed_courses):
    """
    Check if prerequisites are satisfied based on completed courses.
    
    Args:
        prerequisite_string (str): Prerequisite string like "Option 1 or Option 2".
        completed_courses (list): List of courses already completed by the user.
        
    Returns:
        bool: True if prerequisites are satisfied, otherwise False.
    """
    if not prerequisite_string:  # No prerequisites
        return True
    
    prerequisites = prerequisite_string.split(" or ")
    for group in prerequisites:
        group_courses = group.split(", ")
        # Check if all courses in this group are completed
        if all(course.strip() in completed_courses for course in group_courses):
            return True
    return False

# Helper function: Recommend courses based on user interests
def recommend_courses(interests, courses_df):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(courses_df['description'])
    user_vector = vectorizer.transform([interests])
    similarity_scores = cosine_similarity(user_vector, tfidf_matrix).flatten()
    courses_df['similarity'] = similarity_scores
    return courses_df.sort_values(by='similarity', ascending=False)

# Generate schedule
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
            
            prerequisites = course['prerequisites']
            if check_prerequisites(prerequisites, completed_courses):
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
