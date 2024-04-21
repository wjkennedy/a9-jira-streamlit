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
    'Value': []  # Use priority ID as the value for the Sankey flow, if available
}

for issue in issues:
    project = issue['fields']['project']['name']
    issue_type = issue['fields']['issuetype']['name']
    status = issue['fields']['status']['name']
    
    # Safely get the priority ID, default to 0 if not available
    priority_id = int(issue['fields'].get('priority', {}).get('id', 0))

    # Link project to issue type
    sankey_data['Source'].append(project)
    sankey_data['Target'].append(issue_type)
    sankey_data['Value'].append(priority_id)

    # Link issue type to status
    sankey_data['Source'].append(issue_type)
    sankey_data['Target'].append(status)
    sankey_data['Value'].append(priority_id)

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
