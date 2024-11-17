import pandas as pd
from sentence_transformers import SentenceTransformer, util


def load_data(courses_file, requirements_file):
    """Load courses and requirements data from CSV files."""
    courses_df = pd.read_csv(courses_file)
    requirements_df = pd.read_csv(requirements_file)
    return courses_df, requirements_df


def find_relevant_courses(input_interest, courses_df):
    """Find courses relevant to the student's interest using a similarity model."""
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Combine title and description for comparison, handle missing values
    courses_df['combined'] = courses_df['title'].fillna('') + " " + courses_df['description'].fillna('')
    courses_df['combined'] = courses_df['combined'].astype(str)  # Ensure all entries are strings

    # Encode the user's input interest
    user_preference_embedding = model.encode(input_interest, convert_to_tensor=True)

    # Create a copy of the DataFrame to ensure no warnings
    relevant_courses = courses_df.copy()

    # Compute similarity scores for all courses
    relevant_courses.loc[:, 'similarity'] = relevant_courses['combined'].apply(
        lambda text: util.pytorch_cos_sim(user_preference_embedding, model.encode(text, convert_to_tensor=True))[0].item()
    )
    
    # Sort by relevance and return
    return relevant_courses.sort_values(by='similarity', ascending=False)


def check_prerequisites(course_prerequisites, taken_courses, relevant_courses):
    """Check if the prerequisites are satisfied and add them if necessary."""
    if pd.isna(course_prerequisites) or course_prerequisites.strip() == "":
        return True, []

    prerequisites = course_prerequisites.split(",")
    unmet_prereqs = []
    for prereq in prerequisites:
        if "and" in prereq.lower():
            # All 'and' prerequisites must be taken
            and_courses = [c.strip() for c in prereq.split("and")]
            if not all(course in taken_courses for course in and_courses):
                unmet_prereqs.extend(and_courses)
        else:
            # Any one of the prerequisites is sufficient
            options = [course.strip() for course in prereq.split("or")]
            if not any(course in taken_courses for course in options):
                # Choose the most relevant prerequisite based on similarity
                relevant_prereqs = relevant_courses[relevant_courses['title'].isin(options)]
                if not relevant_prereqs.empty:
                    unmet_prereqs.append(relevant_prereqs.iloc[0]['title'])

    return len(unmet_prereqs) == 0, unmet_prereqs


def allocate_courses(courses_df, requirements_df, max_credits_per_semester):
    """Create a semester-wise course plan based on requirements and credits."""
    total_credits = 0
    semesters = []
    taken_courses = set()
    
    # Iterate through each category and subcategory
    for _, req_row in requirements_df.iterrows():
        category = req_row['Category']
        subcategory = req_row['Subcategory']
        required_courses = [c.strip() for c in req_row['Courses'].split(",")]
        num_required = int(req_row['Number of Courses'])
        
        # Filter relevant courses and sort by similarity
        subcategory_courses = courses_df[courses_df['title'].isin(required_courses)].copy()
        subcategory_courses = subcategory_courses.sort_values(by='similarity', ascending=False)
        
        allocated = 0
        # Allocate courses until the required number is reached
        while allocated < num_required:
            # Iterate through each course in the subcategory
            for _, course in subcategory_courses.iterrows():
                # Check if the course can be taken based on prerequisites and credit limit
                if course['title'] not in taken_courses and total_credits + course['credits'] <= 60:
                    # Check prerequisites
                    prereqs_satisfied, unmet_prereqs = check_prerequisites(course['prerequisites'], taken_courses, courses_df)

                    # Add unmet prerequisites if necessary
                    for prereq in unmet_prereqs:
                        # Find the course in the DataFrame
                        prereq_course = courses_df[courses_df['title'] == prereq]
                        # Ensure the course exists and hasn't been taken
                        if not prereq_course.empty:
                            # Convert the course to a dictionary
                            prereq_course = prereq_course.iloc[0].to_dict()
                            # Check if the course can be taken based on credits
                            if prereq_course['title'] not in taken_courses:
                                # Add the course to the plan
                                taken_courses.add(prereq_course['title'])
                                # Update total credits
                                total_credits += prereq_course['credits']
                                
                                if not semesters or sum(c['credits'] for c in semesters[-1]) + prereq_course['credits'] > max_credits_per_semester:
                                    semesters.append([])  # Start a new semester
                                semesters[-1].append(prereq_course)

                    # Add the main course after prerequisites
                    if prereqs_satisfied or not unmet_prereqs:
                        taken_courses.add(course['title'])
                        total_credits += course['credits']
                        
                        if not semesters or sum(c['credits'] for c in semesters[-1]) + course['credits'] > max_credits_per_semester:
                            semesters.append([])  # Start a new semester
                        semesters[-1].append(course.to_dict())
                        allocated += 1
                        break
    return semesters


def generate_degree_plan(input_interest, max_credits_per_semester, courses_file, requirements_file):
    """Generate a semester-wise degree plan based on user input."""
    courses_df, requirements_df = load_data(courses_file, requirements_file)
    relevant_courses = find_relevant_courses(input_interest, courses_df)
    semesters = allocate_courses(relevant_courses, requirements_df, max_credits_per_semester)
    
    # Format the output
    for i, semester in enumerate(semesters, 1):
        print(f"\nSemester {i}:")
        for course in semester:
            print(f"  {course['title']} ({course['credits']} credits) - {course['description']}")


# Example usage
if __name__ == "__main__":
    courses_file = "data/cs_courses.csv"
    requirements_file = "data/cs_requirements.csv"
    input_interest = input("Enter your area of interest (e.g., 'AI', 'Networks'): ").strip()
    max_credits_per_sem = int(input("Enter maximum credits per semester: ").strip())
    
    generate_degree_plan(input_interest, max_credits_per_sem, courses_file, requirements_file)
