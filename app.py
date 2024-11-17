from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load the CSV file and specify the 'credits' column as integers
courses_df = pd.read_csv("cs_courses.csv", dtype={"credits": int})
requirements_df = pd.read_csv("cs_requirements.csv")

# Helper function: Check prerequisites
def check_prerequisites(prerequisite_string, completed_courses):
    if not prerequisite_string:  # No prerequisites
        return True
    
    prerequisites = prerequisite_string.split(" or ")
    for group in prerequisites:
        group_courses = group.split(", ")
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

# Map course prerequisites
def map_course_prerequisites(courses_df):
    prereq_map = {}
    for _, row in courses_df.iterrows():
        course = row['title']
        prereq_string = row.get('prerequisites', '')
        if pd.isna(prereq_string) or not prereq_string:
            prereq_map[course] = set()
        else:
            prereq_set = set()
            for group in prereq_string.split(" or "):
                group_courses = {course.strip() for course in group.split(",")}
                prereq_set.update(group_courses)
            prereq_map[course] = prereq_set
    return prereq_map

prereq_map = map_course_prerequisites(courses_df)

# Generate schedule
def generate_schedule(user_data):
    max_credits = user_data['credits_per_semester']
    transfer_credits = user_data['transfer_credits']
    completed_courses = set(user_data['completed_courses'])
    interests = user_data['interests']
    
    # Filter courses based on interests
    recommended_courses = recommend_courses(interests, courses_df)
    
    # Create a schedule
    schedule = []
    remaining_requirements = requirements_df.copy()
    total_credits = transfer_credits

    for semester in range(1, 9):
        semester_credits = 0
        semester_courses = []
        
        for _, course in recommended_courses.iterrows():
            if semester_credits + int(course['credits']) > max_credits:
                break
            if course['title'] in completed_courses:
                continue
            
            # Check prerequisites from the map
            course_title = course['title']
            prerequisites = prereq_map.get(course_title, set())
            if prerequisites.issubset(completed_courses):
                semester_courses.append(course)
                semester_credits += course['credits']
                completed_courses.add(course_title)
                total_credits += course['credits']
                
                # Update remaining requirements
                for _, req in remaining_requirements.iterrows():
                    if course_title in req['Courses']:
                        req['Number needed'] -= 1

        # Sort semester courses by course numbers
        semester_courses = sorted(semester_courses, key=lambda c: int(''.join(filter(str.isdigit, c['title']))))

        # Add sorted courses to the schedule
        schedule.append({'Semester': semester, 'Courses': [c['title'] for c in semester_courses], 'Credits': semester_credits})

        if total_credits >= 120:
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
