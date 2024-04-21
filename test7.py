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
    'Value': [],
    'Hovertext': []  # Adding hover text data
}

for issue in issues:
    project = issue['fields']['project']['name']
    issue_type = issue['fields']['issuetype']['name']
    status = issue['fields']['status']['name']
    priority_id = int(issue['fields'].get('priority', {}).get('id', 0))
    summary = issue['fields'].get('summary', 'No summary available')  # Extracting summary for hover

    # Link project to issue type
    sankey_data['Source'].append(project)
    sankey_data['Target'].append(issue_type)
    sankey_data['Value'].append(priority_id)
    sankey_data['Hovertext'].append(f"Summary: {summary}")  # Add hover text

    # Link issue type to status
    sankey_data['Source'].append(issue_type)
    sankey_data['Target'].append(status)
    sankey_data['Value'].append(priority_id)
    sankey_data['Hovertext'].append(f"Summary: {summary}")  # Reuse hover text for simplicity

# Creating DataFrame
df_sankey = pd.DataFrame(sankey_data)

# Create source-target mapping for nodes
label_list = pd.concat([df_sankey['Source'], df_sankey['Target']]).unique()
label_dict = {label: idx for idx, label in enumerate(label_list)}

# Map text labels to integers
df_sankey['Source'] = df_sankey['Source'].map(label_dict)
df_sankey['Target'] = df_sankey['Target'].map(label_dict)

# Create the Sankey diagram with hover information
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color='black', width=0.5),
        label=label_list,
        color='blue',
        hoverinfo='text',
        hovertext=[f"{label}" for label in label_list]  # Basic hovertext for nodes
    ),
    link=dict(
        source=df_sankey['Source'],
        target=df_sankey['Target'],
        value=df_sankey['Value'],
        hoverinfo='text',
        hovertext=df_sankey['Hovertext']  # Detailed hovertext for links
    )
)])

fig.update_layout(title_text="JIRA Issue Flow Sankey Diagram", font_size=10)
fig.show()
