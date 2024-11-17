import pandas as pd
import re

# Load the CSV file
input_file = "cs_courses.csv"  # Replace with the path to your file
output_file = "cs_courses.csv"

# Read the CSV file
df = pd.read_csv(input_file)

# Function to extract the lower range of credits and convert to integer
def extract_lower_credit(credit_string):
    if pd.isna(credit_string):  # Check if the value is NaN
        return None
    # Extract numbers from the string
    numbers = re.findall(r'\d+', credit_string)
    if numbers:  # If numbers are found, take the first one as the lower range
        return int(numbers[0])
    return None  # Return None if no numbers are found

# Apply the function to the 'credits' column
df['credits'] = df['credits'].apply(extract_lower_credit)

# Save the modified DataFrame to a new CSV file
df.to_csv(output_file, index=False)

print(f"Updated file with integer credits saved to {output_file}")
