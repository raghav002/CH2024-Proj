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


def build_prerequisite_tree(courses_df):
    """Build a tree-like structure for prerequisites."""
    prereq_tree = {}
    for _, course in courses_df.iterrows():
        course_title = course['title']
        prerequisites = course['prerequisites']
        
        if pd.isna(prerequisites) or prerequisites.strip() == "":
            prereq_tree[course_title] = []  # No prerequisites
        else:
            prereq_tree[course_title] = [p.strip() for p in prerequisites.split(",")]
    
    return prereq_tree


def resolve_prerequisites(course_title, taken_courses, prereq_tree, resolved_courses):
    """Resolve prerequisites for a course using DFS."""
    if course_title in taken_courses:
        return []  # Course already taken

    if course_title not in prereq_tree or not prereq_tree[course_title]:
        return [course_title]  # No prerequisites, return this course

    needed_courses = []
    for prereq in prereq_tree[course_title]:
        # Recursively resolve each prerequisite
        if prereq not in taken_courses:
            needed_courses.extend(resolve_prerequisites(prereq, taken_courses, prereq_tree, resolved_courses))

    # Add the main course after its prerequisites
    needed_courses.append(course_title)
    resolved_courses.add(course_title)

    return needed_courses


def allocate_courses(courses_df, requirements_df, max_credits_per_semester):
    """Create a semester-wise course plan based on requirements and credits."""
    total_credits = 0
    semesters = []
    taken_courses = set()

    prereq_tree = build_prerequisite_tree(courses_df)
    resolved_courses = set()  # Keep track of already resolved courses

    for _, req_row in requirements_df.iterrows():
        category = req_row['Category']
        subcategory = req_row['Subcategory']
        required_courses = [c.strip() for c in req_row['Courses'].split(",")]
        num_required = int(req_row['Number of Courses'])

        subcategory_courses = courses_df[courses_df['title'].isin(required_courses)].copy()
        subcategory_courses = subcategory_courses.sort_values(by='similarity', ascending=False)

        allocated = 0
        while allocated < num_required:
            for _, course in subcategory_courses.iterrows():
                if course['title'] in taken_courses:
                    continue

                # Resolve prerequisites using the tree system
                prereqs_to_add = resolve_prerequisites(course['title'], taken_courses, prereq_tree, resolved_courses)

                for prereq in prereqs_to_add:
                    if prereq not in taken_courses:
                        prereq_course = courses_df[courses_df['title'] == prereq]
                        if not prereq_course.empty:
                            prereq_course = prereq_course.iloc[0].to_dict()
                            if total_credits + prereq_course['credits'] > 60:
                                continue

                            if not semesters or sum(c['credits'] for c in semesters[-1]) + prereq_course['credits'] > max_credits_per_semester:
                                semesters.append([])
                            semesters[-1].append(prereq_course)
                            taken_courses.add(prereq)
                            total_credits += prereq_course['credits']

                if course['title'] not in taken_courses:
                    if total_credits + course['credits'] > 60:
                        continue

                    if not semesters or sum(c['credits'] for c in semesters[-1]) + course['credits'] > max_credits_per_semester:
                        semesters.append([])
                    semesters[-1].append(course.to_dict())
                    taken_courses.add(course['title'])
                    total_credits += course['credits']
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
