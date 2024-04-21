import json
import pandas as pd
import plotly.graph_objects as go

# Load the data
with open('search.json', 'r') as file:
    data = json.load(file)

# Extracting data
issues = data['issues']
sankey_data = {
    'Source': [],
    'Target': [],
    'Value': []  # Assuming a normalized priority score
}

for issue in issues:
    project = issue['fields']['project']['name']
    issue_type = issue['fields']['issuetype']['name']
    status = issue['fields']['status']['name']
    # Simulating a priority score extraction (replace with actual logic to extract score)
    priority_score = int(issue['fields']['priority']['id'])  # Priority ID as proxy for score
    
    sankey_data['Source'].append(project)
    sankey_data['Target'].append(issue_type)
    sankey_data['Value'].append(priority_score)  # Use priority as value for the flow

    sankey_data['Source'].append(issue_type)
    sankey_data['Target'].append(status)
    sankey_data['Value'].append(priority_score)

# Creating DataFrame
df_sankey = pd.DataFrame(sankey_data)

# Create source-target mapping for nodes
label_list = pd.concat([df_sankey['Source'], df_sankey['Target']]).unique()
label_dict = {label: idx for idx, label in enumerate(label_list)}

# Map text labels to integers
df_sankey['Source'] = df_sankey['Source'].map(label_dict)
df_sankey['Target'] = df_sankey['Target'].map(label_dict)

# Create the Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color='black', width=0.5),
        label=label_list,
        color='blue'
    ),
    link=dict(
        source=df_sankey['Source'],
        target=df_sankey['Target'],
        value=df_sankey['Value']
    )
)])

fig.update_layout(title_text="JIRA Issue Flow Sankey Diagram", font_size=10)
fig.show()
