from jira import JIRA
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

from jira import JIRA, JIRAError

# Setup JIRA client without authentication
def setup_jira_client(server):
    jira_client = JIRA(server=server)
    return jira_client


def fetch_issues_data(jira_client, project_key):
    try:
        issues = jira_client.search_issues(f'project={project_key}')
        # Rest of your data processing code...
    except JIRAError as e:
        st.error(f"Failed to fetch data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error
    issues = jira_client.search_issues(f'key={issue_key}')
    
    data = []
    for issue in issues:
        created = pd.to_datetime(issue.fields.created)
        resolved = pd.to_datetime(issue.fields.resolutiondate) if issue.fields.resolutiondate else None
        resolution_time = (resolved - created).total_seconds() / 86400 if resolved else None  # resolution time in days
        data.append({
            "Type": issue.fields.issuetype.name,
            "Priority": issue.fields.priority.name if issue.fields.priority else "Unprioritized",
            "ResolutionTime": resolution_time,
            "Status": issue.fields.status.name
        })
    
    return pd.DataFrame(data)

def create_sankey(df, column_order=['Type', 'Priority', 'Status', 'ResolutionTime']):
    # Map your columns to numbers
    label_list = []
    for col in column_order:
        label_list.extend(sorted(df[col].unique()))
    
    label_dict = {v: k for k, v in enumerate(label_list)}
    
    # Create links between nodes
    source = []
    target = []
    value = []
    
    for i in range(len(column_order)-1):
        grouped = df.groupby([column_order[i], column_order[i+1]]).size().reset_index(name='Count')
        source.extend(grouped[column_order[i]].map(label_dict).tolist())
        target.extend(grouped[column_order[i+1]].map(label_dict).tolist())
        value.extend(grouped['Count'].tolist())
    
    # Create the Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node = dict(
            pad = 15,
            thickness = 20,
            line = dict(color = "black", width = 0.5),
            label = label_list,
            color = "blue"
        ),
        link = dict(
            source = source,
            target = target,
            value = value
        )
    )])
    
    return fig

def display_sankey(df):
    st.title('Jira Issue Flow')
    column_order = st.sidebar.selectbox("Select View Order:", 
                                        options=[
                                            ["Type", "Priority", "ResolutionTime"], 
                                            ["Priority", "Type", "ResolutionTime"]
                                        ],
                                        format_func=lambda x: " -> ".join(x))
    fig = create_sankey(df, column_order)
    st.plotly_chart(fig, use_container_width=True)

def main():
    st.title("JAC Dashboard")
    server_url = st.sidebar.text_input("Enter Jira server URL:", "https://jira.atlassian.com")
    project_key = st.sidebar.text_input("Enter the project key:", "JRACLOUD")
    
    if st.sidebar.button("Fetch Data"):
        jira_client = setup_jira_client(server_url)
        df = fetch_issues_data(jira_client, project_key)
        if not df.empty:
            fig = create_sankey(df, ['Type', 'Priority', 'ResolutionTime'])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No data found. Please check the project key and ensure it is for a public project.")

if __name__ == "__main__":
    main()
