import pandas as pd
import random

def load_data(reqs_path, courses_path):
    """Load data from CSV files."""
    reqs = pd.read_csv(reqs_path)
    courses = pd.read_csv(courses_path)
    return reqs, courses

def recommend_courses(reqs, courses, interests):
    """
    Recommend courses based on interests and requirements.
    
    Arguments:
        reqs: DataFrame containing course requirements.
        courses: DataFrame containing all course details (title, description, etc.).
        interests: List of interests provided by the user.
        
    Returns:
        List of recommended courses.
    """
    recommendations = []
    
    for _, row in reqs.iterrows():
        category = row['Category']
        required_courses = int(row['Number of Courses'])

        # Filter courses in the given category
        category_courses = courses[courses['title'].str.contains(category, case=False, na=False)]

        # Further filter by interests if provided
        if interests:
            filtered_courses = category_courses[
                category_courses['description'].str.contains('|'.join(interests), case=False, na=False)
            ]
        else:
            filtered_courses = category_courses

        # If not enough courses match interests, fall back to all category courses
        if len(filtered_courses) < required_courses:
            filtered_courses = category_courses

        # Select the required number of courses randomly
        selected_courses = filtered_courses.sample(min(required_courses, len(filtered_courses)), replace=False)
        recommendations.extend(selected_courses.to_dict('records'))
    
    return recommendations

def main():
    # Load the requirements and course catalog
    reqs_path = 'reqs.csv'
    courses_path = 'courses.csv'
    reqs, courses = load_data(reqs_path, courses_path)

    # User input: interests
    print("Enter your interests (e.g., 'machine learning', 'data science'), separated by commas:")
    interests = input().strip().split(',')
    interests = [interest.lower().strip() for interest in interests if interest.strip()]

    # Recommend courses
    recommendations = recommend_courses(reqs, courses, interests)

    # Display recommendations
    print("\nRecommended Courses:")
    for course in recommendations:
        print(f"Title: {course['title']}")
        print(f"Description: {course['description']}")
        print(f"Credits: {course['credits']}")
        print(f"Prerequisites: {course['prerequisites']}")
        print("---")

if __name__ == "__main__":
    main()
