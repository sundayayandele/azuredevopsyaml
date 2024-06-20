import requests
from requests.auth import HTTPBasicAuth
import json
import os

# Replace these values with your Azure DevOps details
organization = 'your-organization'
project = 'your-project'
pat = os.environ['AZURE_DEVOPS_EXT_PAT']  # Using environment variable for security
repo_prefix = 'your-repo-prefix'  # The first 6 letters prefix for your repos

# Base URL for Azure DevOps REST API
base_url = f'https://dev.azure.com/{organization}/{project}/_apis'

# Function to get all pipelines
def get_pipelines():
    pipelines_url = f'{base_url}/pipelines?api-version=6.0'
    response = requests.get(pipelines_url, auth=HTTPBasicAuth('', pat))
    
    if response.status_code == 200:
        return response.json()['value']
    else:
        print(f'Error retrieving pipelines: {response.status_code}')
        return []

# Function to get pipeline details (including repository info)
def get_pipeline_details(pipeline_id):
    pipeline_url = f'{base_url}/pipelines/{pipeline_id}?api-version=6.0'
    response = requests.get(pipeline_url, auth=HTTPBasicAuth('', pat))
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error retrieving pipeline details: {response.status_code}')
        return None

# Function to find pipeline owners based on repo prefix
def find_pipeline_owners():
    pipelines = get_pipelines()
    pipelines_info = []

    for pipeline in pipelines:
        pipeline_id = pipeline['id']
        pipeline_name = pipeline['name']
        
        details = get_pipeline_details(pipeline_id)
        if details:
            repo_name = details['repository']['name']
            if repo_name.startswith(repo_prefix):
                # Assuming the pipeline owner info can be found in the 'createdBy' field
                owner = details['createdBy']['displayName']
                pipelines_info.append({'Pipeline Name': pipeline_name, 'Owner': owner})
    
    return pipelines_info

# Get the list of pipelines and their owners
pipelines_info = find_pipeline_owners()

# Save the result to a JSON file
with open('pipelines_info.json', 'w') as f:
    json.dump(pipelines_info, f, indent=2)

# Print the result for logging purposes
for info in pipelines_info:
    print(f"Pipeline: {info['Pipeline Name']}, Owner: {info['Owner']}")
