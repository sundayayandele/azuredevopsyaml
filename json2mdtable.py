import json
import os
import requests

def get_access_token():
    """Retrieve the Azure DevOps access token from environment variable."""
    return os.getenv('SYSTEM_ACCESSTOKEN')

def get_user_descriptor(display_name, organization):
    """Get the user descriptor using user entitlements API."""
    access_token = get_access_token()
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    filter_name = f"name eq '{display_name}'"
    url = f"https://vsaex.dev.azure.com/{organization}/_apis/userentitlements?$filter={filter_name}&api-version=7.1-preview-3"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        entitlements = response.json()
        if 'value' in entitlements and len(entitlements['value']) > 0:
            user_descriptor = entitlements['value'][0]['user']['descriptor']
            return user_descriptor
        else:
            print(f"No user entitlement found for display name: {display_name}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving user entitlement: {e}")
        return None

def get_user_memberships(user_descriptor, organization):
    """Get user memberships using the user descriptor."""
    access_token = get_access_token()
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    url = f"https://vsaex.dev.azure.com/{organization}/_apis/graph/users/{user_descriptor}/memberships?api-version=7.1-preview.1"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        memberships = response.json()
        if 'value' in memberships:
            return [membership['displayName'] for membership in memberships['value']]
        else:
            print(f"No memberships found for user descriptor: {user_descriptor}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving user memberships: {e}")
        return []

def get_pipelines(organization, project, folder_path):
    """Get all pipelines from a specific folder."""
    access_token = get_access_token()
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    url = f"https://dev.azure.com/{organization}/{project}/_apis/build/definitions?path={folder_path}&api-version=6.0"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving pipelines: {e}")
        return None

def get_pipeline_details(organization, project, pipeline_id):
    """Get detailed pipeline information."""
    access_token = get_access_token()
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    url = f"https://dev.azure.com/{organization}/{project}/_apis/pipelines/{pipeline_id}?api-version=6.0-preview.1"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving pipeline details: {e}")
        return None

def find_pipeline_details(organization, project, folder_paths):
    """Get pipeline details from the specified folders."""
    pipeline_details = []

    for folder_path in folder_paths:
        pipelines = get_pipelines(organization, project, folder_path)
        if pipelines is None or 'value' not in pipelines:
            print(f"No pipelines found for folder: {folder_path}")
            continue

        for pipeline in pipelines['value']:
            pipeline_id = pipeline['id']
            repository_name = pipeline.get('repository', {}).get('name', 'Unknown')
            author_name = pipeline.get('createdBy', {}).get('displayName', 'Unknown')
            created_date = pipeline.get('createdDate', 'Unknown')
            if author_name:
                author_descriptor = get_user_descriptor(author_name, organization)
                if author_descriptor:
                    author_memberships = get_user_memberships(author_descriptor, organization)
                else:
                    author_memberships = []
            else:
                author_memberships = []

            pipeline_detail = get_pipeline_details(organization, project, pipeline_id)
            if pipeline_detail:
                pipeline_name = pipeline_detail['name']
                yaml_file_name = pipeline_detail.get('configuration', {}).get('path', 'Unknown')

                pipeline_details.append({
                    'Pipeline Name': pipeline_name,
                    'Repository Name': repository_name,
                    'YAML File Name': yaml_file_name,
                    'Author': author_name,
                    'Created Date': created_date,
                    'Author Memberships': author_memberships
                })

    return pipeline_details

def convert_to_markdown_table(pipeline_details):
    """Convert pipeline details to a markdown table."""
    md_lines = [
        "| Pipeline Name | Repository Name | YAML File Name | Author | Created Date | Author Memberships |",
        "| ------------- | --------------- | -------------- | ------ | ------------ | ------------------ |"
    ]
    for detail in pipeline_details:
        memberships = ', '.join(detail['Author Memberships'])
        md_lines.append(
            f"| {detail['Pipeline Name']} | {detail['Repository Name']} | {detail['YAML File Name']} | {detail['Author']} | {detail['Created Date']} | {memberships} |"
        )
    return "\n".join(md_lines)

if __name__ == "__main__":
    organization = 'SAAM'
    project = 'Abc'
    folder_filters = ['\\S0123\\abc', '\\S0123\\def', '\\S0123\\aba', '\\S0123\\riso', '\\S0123\\ahs', '\\S0123\\eid']

    pipeline_details = find_pipeline_details(organization, project, folder_filters)

    # Save to JSON file
    with open('pipeline_details.json', 'w') as f:
        json.dump(pipeline_details, f, indent=2)

    # Convert to markdown table and save to .md file
    md_content = convert_to_markdown_table(pipeline_details)
    with open('pipeline_details.md', 'w') as f:
        f.write(md_content)

    for detail in pipeline_details:
        print(f"Pipeline Name: {detail['Pipeline Name']}, Repository Name: {detail['Repository Name']}, YAML File Name: {detail['YAML File Name']}, Author: {detail['Author']}, Created Date: {detail['Created Date']}, Author Memberships: {', '.join(detail['Author Memberships'])}")




==============================================================
trigger:
- main

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: UsePythonVersion@0
  inputs:
    versionSpec: '3.x'
    addToPath: true

- script: |
    python -m pip install requests
  displayName: 'Install dependencies'

- script: |
    python get_pipeline_details.py
  displayName: 'Get Pipeline Details'
  env:
    SYSTEM_ACCESSTOKEN: $(System.AccessToken)

- script: |
    sudo apt-get update
    sudo apt-get install -y jq
    sudo wget https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64 -O /usr/bin/yq
    sudo chmod +x /usr/bin/yq
  displayName: 'Install jq and yq'

- script: |
    jq -r '["Pipeline Name", "Repository Name", "YAML File Name", "Author", "Author Memberships"], (.[] | [.["Pipeline Name"], .["Repository Name"], .["YAML File Name"], .["Author"], (.["Author Memberships"] | join(", "))]) | @csv' pipeline_details.json > pipeline_details.csv

    yq eval -P '. | 
    "## Pipeline Details\n" + 
    "| Pipeline Name | Repository Name | YAML File Name | Author | Author Memberships |\n| ------------- | --------------- | -------------- | ------ | ------------------ |\n" +
    (.[] | "| " + .["Pipeline Name"] + " | " + .["Repository Name"] + " | " + .["YAML File Name"] + " | " + .["Author"] + " | " + (.["Author Memberships"] | join(", ")) + " |\n")' pipeline_details.json > pipeline_details.md
  displayName: 'Convert JSON to CSV and Markdown'

- publish: pipeline_details.csv
  artifact: pipeline-details-csv
  displayName: 'Publish Pipeline Details CSV'

- publish: pipeline_details.md
  artifact: pipeline-details-markdown
  displayName: 'Publish Pipeline Details Markdown'

========================================================
import json
import pandas as pd

def generate_json():
    # Example data to be saved in JSON
    pipeline_details = [
        {
            "Pipeline Name": "Pipeline1",
            "Repository Name": "Repo1",
            "Author": "Author1",
            "Author Memberships": ["Group1", "Group2"],
            "Team Memberships": ["Team1", "Team2"]
        },
        {
            "Pipeline Name": "Pipeline2",
            "Repository Name": "Repo2",
            "Author": "Author2",
            "Author Memberships": ["Group3"],
            "Team Memberships": ["Team3"]
        }
    ]

    # Save to JSON file
    with open('pipeline_details.json', 'w') as f:
        json.dump(pipeline_details, f, indent=2)

def json_to_md():
    # Load data from JSON file
    with open('pipeline_details.json', 'r') as f:
        data = json.load(f)

    # Normalize the data to flatten lists into comma-separated strings
    for item in data:
        item['Author Memberships'] = ', '.join(item['Author Memberships'])
        item['Team Memberships'] = ', '.join(item['Team Memberships'])

    # Convert data to DataFrame
    df = pd.DataFrame(data)

    # Convert DataFrame to Markdown table
    md_table = df.to_markdown(index=False)

    # Save to Markdown file
    with open('pipeline_details.md', 'w') as f:
        f.write(md_table)

    # Print the Markdown table for logging purposes
    print(md_table)

# Execute functions sequentially
generate_json()
json_to_md()



==================================
import json
import pandas as pd

def generate_json():
    # Example data to be saved in JSON
    pipeline_details = [
        {
            "Pipeline Name": "Pipeline1",
            "Repository Name": "Repo1",
            "Author": "Author1",
            "Author Memberships": ["Group1", "Group2"],
            "Team Memberships": ["Team1", "Team2"]
        },
        {
            "Pipeline Name": "Pipeline2",
            "Repository Name": "Repo2",
            "Author": "Author2",
            "Author Memberships": ["Group3"],
            "Team Memberships": ["Team3"]
        }
    ]

    # Save to JSON file
    with open('pipeline_details.json', 'w') as f:
        json.dump(pipeline_details, f, indent=2)

def json_to_md():
    # Load data from JSON file
    with open('pipeline_details.json', 'r') as f:
        data = json.load(f)

    # Normalize the data to flatten lists into comma-separated strings
    for item in data:
        item['Author Memberships'] = ', '.join(item['Author Memberships'])
        item['Team Memberships'] = ', '.join(item['Team Memberships'])

    # Convert data to DataFrame
    df = pd.DataFrame(data)

    # Convert DataFrame to Markdown table
    md_table = df.to_markdown(index=False)

    # Save to Markdown file
    with open('pipeline_details.md', 'w') as f:
        f.write(md_table)

if __name__ == "__main__":
    generate_json()
    json_to_md()
