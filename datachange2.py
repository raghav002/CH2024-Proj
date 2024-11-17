import pandas as pd

# Load the CSV file
input_file = "cs_courses.csv"
output_file = "modified_cs_courses.csv"

# Read the CSV file
df = pd.read_csv(input_file)

# Extract course numbers from the title
df['title'] = df['title'].str.extract(r'(\bCOMP SCI\b.*?—|\bCOMP SCI\b.*?—|MATH\b.*?—|STAT\b.*?—)')[0].str.split('—').str[0].str.strip()

# Save the updated DataFrame to a new CSV file
df.to_csv(output_file, index=False)

print("Titles have been updated to contain only course numbers. The modified file is saved as 'modified_cs_courses.csv'.")
