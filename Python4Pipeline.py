import requests

# Constants
ORG_URL = 'https://dev.azure.com/your_org'
PROJECT = 'SaOne'
TOKEN = 'your_personal_access_token'

# Headers
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Basic {TOKEN}'
}

# Get all group permissions
def get_group_permissions():
    url = f'{ORG_URL}/_apis/graph/groups?api-version=6.0-preview.1'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['value']

# Get all pipelines with details
def get_pipelines():
    url = f'{ORG_URL}/{PROJECT}/_apis/pipelines?api-version=7.0'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['value']

# Get pipeline details
def get_pipeline_details(pipeline_id):
    url = f'{ORG_URL}/{PROJECT}/_apis/pipelines/{pipeline_id}?api-version=7.0'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Get pipeline runs to extract user descriptors
def get_pipeline_runs(pipeline_id):
    url = f'{ORG_URL}/{PROJECT}/_apis/pipelines/{pipeline_id}/runs?api-version=7.0'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['value']

# Match users to groups
def match_users_to_groups(user_descriptor, groups):
    matched_groups = [group['principalName'] for group in groups if user_descriptor in group.get('members', [])]
    return matched_groups

# Main execution
def main():
    groups = get_group_permissions()
    pipelines = get_pipelines()
    
    # Filter groups by prefix
    inner_groups = [group for group in groups if group['principalName'].startswith('SAAM')]

    for pipeline in pipelines:
        pipeline_id = pipeline['id']
        details = get_pipeline_details(pipeline_id)
        runs = get_pipeline_runs(pipeline_id)
        
        for run in runs:
            creator = run['createdBy']['descriptor']
            creation_date = run['createdDate']
            last_update_date = run['lastChangedDate']
            repo_name = details['configuration']['repository']['name']
            yaml_path = details['configuration']['path']
            
            # Match user to inner groups
            matched_groups = match_users_to_groups(creator, inner_groups)
            
            print(f"Pipeline ID: {pipeline_id}")
            print(f"Creator: {creator}")
            print(f"Creation Date: {creation_date}")
            print(f"Last Update: {last_update_date}")
            print(f"Repo Name: {repo_name}")
            print(f"YAML Path: {yaml_path}")
            print(f"Inner Permission Groups: {matched_groups}")
            print('-' * 40)

if __name__ == "__main__":
    main()
