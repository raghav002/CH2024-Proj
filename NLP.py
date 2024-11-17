import pandas as pd
from sentence_transformers import SentenceTransformer, util


def load_data(courses_file, requirements_file):
    """Load courses and requirements data from CSV files."""
    courses_df = pd.read_csv(courses_file)
    courses_df = pd.read_csv(courses_file, dtype={"credits": "int"})
    requirements_df = pd.read_csv(requirements_file)
    return courses_df, requirements_df


def find_relevant_courses(input_interest, courses_df):
    """Find courses relevant to the student's interest using a similarity model."""
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Combine title and description for comparison
    courses_df['combined'] = courses_df['title'] + " " + courses_df['description']
    input_embedding = model.encode(input_interest, convert_to_tensor=True)
    course_embeddings = model.encode(courses_df['combined'].tolist(), convert_to_tensor=True)
    
    # Compute similarity scores
    similarities = util.pytorch_cos_sim(input_embedding, course_embeddings)[0]
    courses_df['similarity'] = similarities.cpu().numpy()
    
    # Sort by relevance
    print(courses_df)
    return courses_df.sort_values(by='similarity', ascending=False)


def check_prerequisites(course_prerequisites, taken_courses):
    """Check if the prerequisites are satisfied."""
    # If no prerequisites are listed, return True
    if pd.isna(course_prerequisites) or course_prerequisites.strip() == "":
        return True  # No prerequisites
    # Split prerequisites into individual courses
    prerequisites = course_prerequisites.split(",") 
    # Check if all prerequisites are satisfied
    for prereq in prerequisites:
        # Check if "and" is present in the prerequisite
        if "and" in prereq.lower():
            # All courses listed with 'and' are required
            and_courses = [c.strip() for c in prereq.split("and")]
            if all(course in taken_courses for course in and_courses):
                return True
        else:
            # Only one of the listed prerequisites is required
            if any(course.strip() in taken_courses for course in prerequisites):
                return True
    return False


def allocate_courses(courses_df, requirements_df, max_credits_per_semester):
    """Create a semester-wise course plan based on requirements and credits."""
    total_credits = 0
    semesters = []
    taken_courses = set()
    
    # Iterate through each category and subcategory
    for _, req_row in requirements_df.iterrows():
        category = req_row['Category']
        subcategory = req_row['Subcategory']
        #print(req_row['Courses'])
        required_courses = [c.strip() for c in req_row['Courses'].split(",")]  # Split list of course options
        #print(required_courses)
        num_required = int(req_row['Number of Courses'])
        #print(num_required)
        
        # Filter relevant courses and sort by similarity
        subcategory_courses = courses_df[courses_df['title'].isin(required_courses)]
        print (subcategory_courses)
        subcategory_courses = subcategory_courses.sort_values(by='similarity', ascending=False)
        # Allocate required number of courses
        allocated = 0
        # While the number of courses allocated from this subcat haven't reached the required number
        # and while there are still courses in this subcat
        while allocated < num_required:
            # Iterate through each course in the subcategory
            for _, course in subcategory_courses.iterrows():
                # Check if the course hasn't been taken and the total credits won't exceed the limit
                if course['title'] not in taken_courses and total_credits + course['credits'] <= 60:
                    # Check if prerequisites are satisfied
                    if check_prerequisites(course['prerequisites'], taken_courses):
                        # Add the course to the plan
                        taken_courses.add(course['title']) 
                        # Update total credits
                        total_credits += course['credits']
                        
                        # Assign to a semester
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
