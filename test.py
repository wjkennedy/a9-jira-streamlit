import json
import pandas as pd

# Load JSON data (assuming JSON data is loaded into a variable `data`)
with open('search.json', 'r') as file:
    data = json.load(file)

# Initialize lists to store extracted data
issues_data = []

# Process each issue in the JSON data
for issue in data['issues']:
    issue_type = issue['fields'].get('issuetype', {}).get('name', 'No Type')
    priority = issue['fields'].get('priority', {}).get('name', 'No Priority')
    status = issue['fields'].get('status', {}).get('name', 'No Status')
    project = issue['fields'].get('project', {}).get('name', 'No Project')

    # Append to list as a dictionary
    issues_data.append({
        'Issue Type': issue_type,
        'Priority': priority,
        'Status': status,
        'Project': project
    })

# Convert list of dicts to DataFrame
df = pd.DataFrame(issues_data)

# Output the DataFrame to see the data
print(df.head())

import streamlit as st

def display_data(df):
    st.write("## Issue Data Overview")
    st.write(df)  # Display the DataFrame in the app

def main():
    st.title("Jira Data Visualization Dashboard")
    # Assuming `df` is the DataFrame we prepared earlier
    display_data(df)

if __name__ == "__main__":
    main()
