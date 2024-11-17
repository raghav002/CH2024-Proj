from app.database import get_connection
import requests
from bs4 import BeautifulSoup
import re

def scrape_courses():
    url = "https://guide.wisc.edu/courses/comp_sci/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Function to clean text (removes ZWS and non-breaking spaces)
    def clean_text(text):
        return text.replace("\xa0", " ").replace("\u200b", "").strip()

    # Function to extract valid course names from prerequisites
    def extract_course_names(prerequisite_text):
        # Regex pattern to match valid course names like "COMP SCI 300", "MATH 96", etc.
        pattern = r'\b[A-Za-z]+\s\d{2,3}\b'
        courses = re.findall(pattern, prerequisite_text)
        return courses
    
    def clean_credits(raw_credits):
        if raw_credits:
            # Remove 'credits.' or 'credit.'
            cleaned = raw_credits.replace(' credits.', '').replace(' credit.', '').strip()
            # Split by '-' for ranges and take the minimum value
            min_credit = cleaned.split('-')[0]
            try:
                return int(min_credit)  # Convert to integer
            except ValueError:
                return 0  # Default to 0 if conversion fails
        return 0

    courses = []
    for course in soup.find_all("div", class_="courseblock"):
        coursenum = course.find('span', class_='courseblockcode').text.strip()
        title = clean_text(course.find('p', class_='courseblocktitle').text) if course.find('p', class_='courseblocktitle') else "None"
        description = clean_text(course.find('p', class_='courseblockdesc').text) if course.find('p', class_='courseblockdesc') else "None"
        credits_raw = course.find('p', class_='courseblockcredits').text if course.find('p', class_='courseblockcredits') else "0"
        credits = clean_credits(credits_raw)        
        prerequisites_text = clean_text(course.find('p', class_='courseblockextra').text) if course.find('p', class_='courseblockextra') else "None"
        prerequisites = extract_course_names(prerequisites_text)  # Extract course names only
        courses.append((coursenum, title, description, credits, prerequisites))

    return courses

def update_database():
    courses = scrape_courses()
    conn = get_connection()
    cursor = conn.cursor()

    for course in courses:
        cursor.execute("""
        INSERT OR REPLACE INTO courses (course_code, title, description, credits, prerequisites)
        VALUES (?, ?, ?, ?, ?)
        """, course)

    conn.commit()
    conn.close()
