import pandas as pd

# Load the CSV file
courses_df = pd.read_csv("data/cs_courses.csv")

# Extract the numeric part of the 'credits' column and convert to int
courses_df['credits'] = courses_df['credits'].str.extract(r'(\d+)').astype(int)

# Save the updated DataFrame back to the CSV (optional)
courses_df.to_csv("data/cs_courses.csv", index=False)

# Verify the updated DataFrame
print(courses_df.head())
