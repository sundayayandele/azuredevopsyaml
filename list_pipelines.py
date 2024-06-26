# Function to get user descriptor using userentitlements API
def get_user_descriptor(user_id, token):
    user_entitlements_url = f'{entitlements_api_url}?api-version=6.0-preview'
    response = requests.get(user_entitlements_url, headers={'Authorization': f'Bearer {token}'})
    
    if response.status_code == 200:
        entitlements = response.json().get('value', [])
        for entitlement in entitlements:
            user = entitlement.get('user', {})
            if user.get('subjectkind') == 'user' and user.get('id') == user_id:
                return user.get('descriptor')
        print(f'User descriptor not found for user ID: {user_id}')
        return None
    else:
        print(f'Error retrieving user entitlements: {response.status_code}, {response.text}')
        return None

# Function to get user memberships
def get_user_memberships(user_descriptor, token):
    memberships_url = f'{entitlements_api_url}/{user_descriptor}/groups?api-version=6.0-preview'
    response = requests.get(memberships_url, headers={'Authorization': f'Bearer {token}'})
    
    if response.status_code == 200:
        memberships = response.json().get('value', [])
        membership_names = [membership['displayName'] for membership in memberships if 'displayName' in membership]
        return membership_names
    else:
        print(f'Error retrieving user memberships: {response.status_code}, {response.text}')
        return []

# Function to recursively get pipeline details from a folder and its subfolders
def find_pipeline_details_recursively(folder_paths, token):
    pipeline_details = []

    def traverse_folders(current_folder):
        pipelines = get_pipelines_from_folder(current_folder, token)
        
        for pipeline in pipelines:
            pipeline_id = pipeline['id']
            details = get_pipeline_details(pipeline_id, token)
            if details:
                pipeline_name = details['name']
                repository_name = details.get('repository', {}).get('name', 'Unknown')
                author_name = details.get('authoredBy', {}).get('displayName', 'Unknown')
                author_id = details.get('authoredBy', {}).get('id', None)
                if author_id:
                    author_descriptor = get_user_descriptor(author_id, token)
                    if author_descriptor:
                        author_memberships = get_user_memberships(author_descriptor, token)
                    else:
                        author_memberships = []
                else:
                    author_memberships = []
                pipeline_details.append({
                    'Pipeline Name': pipeline_name,
                    'Repository Name': repository_name,
                    'Author': author_name,
                    'Author Memberships': author_memberships
                })

        # Check for subfolders and traverse them
        subfolders_url = f'{base_url}?api-version={api_version}&path={current_folder}'
        response = requests.get(subfolders_url, headers={'Authorization': f'Bearer {token}'})
        if response.status_code == 200:
            result = response.json()
            for item in result.get('value', []):
                if item.get('folder', False):
                    traverse_folders(item['path'])
        else:
            print(f'Error retrieving subfolders: {response.status_code}, {response.text}')

    for folder_path in folder_paths:
        traverse_folders(folder_path)
    
    return pipeline_details

# Get the list of pipeline details recursively for multiple folder filters
pipeline_details = find_pipeline_details_recursively(folder_filters, token)

# Save the result to a JSON file
with open('pipeline_details.json', 'w') as f:
    json.dump(pipeline_details, f, indent=2)

# Print the result for logging purposes
for detail in pipeline_details:
    print(f"Pipeline Name: {detail['Pipeline Name']}, Repository Name: {detail['Repository Name']}, Author: {detail['Author']}, Author Memberships: {', '.join(detail['Author Memberships'])}")



================================================
def find_pipeline_owners():
    pipelines = get_pipelines()
    pipelines_info = []

    print(f'Found {len(pipelines)} pipelines')
    for pipeline in pipelines:
        pipeline_id = pipeline['id']
        pipeline_name = pipeline['name']
        
        details = get_pipeline_details(pipeline_id)
        if details:
            repository = details.get('repository', {})
            repo_name = repository.get('name', '')
            
            # Debug information
            print(f'Checking pipeline: {pipeline_name}, Repo Name: {repo_name}')
            
            # Check if the repository name starts with the specified prefix
            if repo_name.startswith(repo_name_prefix):
                owner = details.get('createdBy', {}).get('displayName', 'Unknown')
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
===============================================================================
folder_filter = '\\S0123'  # Adjusted for correct folder path

# Retrieve system access token from the environment
token = os.getenv('SYSTEM_ACCESSTOKEN')

# Function to get all pipelines
def get_pipelines():
    pipelines_url = f'{base_url}?api-version={api_version}'
    print(f'Requesting pipelines from: {pipelines_url}')
    response = requests.get(pipelines_url, headers={'Authorization': f'Bearer {token}'})
    
    if response.status_code == 200:
        return response.json().get('value', [])
    else:
        print(f'Error retrieving pipelines: {response.status_code}, {response.text}')
        return []

# Function to get pipeline details (including repository info)
def get_pipeline_details(pipeline_id):
    pipeline_url = f'{base_url}/{pipeline_id}?api-version={api_version}'
    response = requests.get(pipeline_url, headers={'Authorization': f'Bearer {token}'})
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error retrieving pipeline details: {response.status_code}, {response.text}')
        return None

# Function to find pipeline owners based on folder path
def find_pipeline_owners():
    pipelines = get_pipelines()
    pipelines_info = []

    print(f'Found {len(pipelines)} pipelines')
    for pipeline in pipelines:
        pipeline_id = pipeline['id']
        pipeline_name = pipeline['name']
        folder_path = pipeline.get('path', '')

        # Debug information
        print(f'Checking pipeline: {pipeline_name}, Path: {folder_path}')
        
        # Check if the pipeline is in the specified folder
        if folder_path.startswith(folder_filter):
            details = get_pipeline_details(pipeline_id)
            if details:
                owner = details.get('createdBy', {}).get('displayName', 'Unknown')
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

=======================================================================================================================
def get_pipelines():
    pipelines_url = f'{base_url}?api-version={api_version}'
    response = requests.get(pipelines_url, headers={'Authorization': f'Bearer {token}'})
    
    if response.status_code == 200:
        return response.json()['value']
    else:
        print(f'Error retrieving pipelines: {response.status_code}, {response.text}')
        return []

# Function to get pipeline details (including repository info)
def get_pipeline_details(pipeline_id):
    pipeline_url = f'{base_url}/{pipeline_id}?api-version={api_version}'
    response = requests.get(pipeline_url, headers={'Authorization': f'Bearer {token}'})
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error retrieving pipeline details: {response.status_code}, {response.text}')
        return None

# Function to find pipeline owners based on pipeline name filter
def find_pipeline_owners():
    pipelines = get_pipelines()
    pipelines_info = []

    print(f'Found {len(pipelines)} pipelines')
    for pipeline in pipelines:
        pipeline_id = pipeline['id']
        pipeline_name = pipeline['name']
        folder_path = pipeline['path']
        
        # Debug information
        print(f'Checking pipeline: {pipeline_name}, Path: {folder_path}')
        
        # Check if the pipeline is in the specified folder
        if folder_path.startswith(f'\\{pipeline_name_filter}'):
            details = get_pipeline_details(pipeline_id)
            if details:
                owner = details.get('createdBy', {}).get('displayName', 'Unknown')
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



=====================================================================================
token = os.getenv('SYSTEM_ACCESSTOKEN')

# Function to get all pipelines
def get_pipelines():
    pipelines_url = f'{base_url}?api-version={api_version}'
    response = requests.get(pipelines_url, headers={'Authorization': f'Bearer {token}'})
    
    if response.status_code == 200:
        return response.json()['value']
    else:
        print(f'Error retrieving pipelines: {response.status_code}, {response.text}')
        return []

# Function to get pipeline details (including repository info)
def get_pipeline_details(pipeline_id):
    pipeline_url = f'{base_url}/{pipeline_id}?api-version={api_version}'
    response = requests.get(pipeline_url, headers={'Authorization': f'Bearer {token}'})
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error retrieving pipeline details: {response.status_code}, {response.text}')
        return None

# Function to find pipeline owners based on pipeline name filter
def find_pipeline_owners():
    pipelines = get_pipelines()
    pipelines_info = []

    for pipeline in pipelines:
        pipeline_id = pipeline['id']
        pipeline_name = pipeline['name']
        
        # Check if pipeline name starts with the filter
        if pipeline_name.startswith(pipeline_name_filter):
            details = get_pipeline_details(pipeline_id)
            if details:
                owner = details.get('createdBy', {}).get('displayName', 'Unknown')
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


=============================================================================================
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
    pip install requests
    python - <<EOF
import requests
import json
import os

# Azure DevOps configuration
organization = 'SAAM'
project = 'Abc'
api_version = '6.0'
base_url = f'https://dev.azure.com/{organization}/{project}/_apis'
pipeline_name_filter = 'S0123'

# Retrieve system access token from the environment
token = os.getenv('SYSTEM_ACCESSTOKEN')

# Function to get all pipelines
def get_pipelines():
    pipelines_url = f'{base_url}/pipelines?api-version={api_version}&name={pipeline_name_filter}'
    response = requests.get(pipelines_url, headers={'Authorization': f'Bearer {token}'})
    
    if response.status_code == 200:
        return response.json()['value']
    else:
        print(f'Error retrieving pipelines: {response.status_code}, {response.text}')
        return []

# Function to get pipeline details (including repository info)
def get_pipeline_details(pipeline_id):
    pipeline_url = f'{base_url}/pipelines/{pipeline_id}?api-version={api_version}'
    response = requests.get(pipeline_url, headers={'Authorization': f'Bearer {token}'})
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error retrieving pipeline details: {response.status_code}, {response.text}')
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
            owner = details.get('createdBy', {}).get('displayName', 'Unknown')
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

EOF
  displayName: 'Run Python script to list pipelines'
  env:
    SYSTEM_ACCESSTOKEN: $(System.AccessToken)

- task: PublishBuildArtifacts@1
  inputs:
    PathtoPublish: 'pipelines_info.json'
    ArtifactName: 'pipelines_info'



-----------------------------------------------
import requests
      import yaml

      def get_pipelines_and_ownership(organization_url, personal_access_token, project_name, repo_prefix):
          """
          Lists pipelines in a project and identifies ownership based on a repository name prefix.

          Args:
              organization_url: URL of your Azure DevOps organization (e.g., https://dev.azure.com/your_organization)
              personal_access_token: PAT with access to read pipelines and repositories
              project_name: Name of the Azure DevOps project
              repo_prefix: The prefix for the repository name (e.g., ab9180)
          """

          # Base URL for Azure DevOps API calls
          base_url = f"{organization_url}/_apis/"

          # Construct API endpoint for listing pipelines
          pipelines_url = f"{base_url}pipelines/pipelines?api-version=6.0-preview.1&project={project_name}"

          # Set headers with PAT for authentication (using system.access token)
          headers = {"Authorization": f"Basic PAT {$(System.AccessToken)}"}

          # Get list of pipelines
          response = requests.get(pipelines_url, headers=headers)

          if response.status_code == 200:
              pipelines_data = response.json()
              pipelines = []

              for pipeline in pipelines_data["value"]:
                  # Get pipeline definition by ID
                  pipeline_id = pipeline["id"]
                  definition_url = f"{base_url}pipelines/{pipeline_id}?$expand=definition&api-version=6.0-preview.1"
                  definition_response = requests.get(definition_url, headers=headers)

                  if definition_response.status_code == 200:
                      definition_data = definition_response.json()
                      definition = definition_data["definition"]

                      # Parse YAML definition to find repository name
                      try:
                          # Assuming YAML definition is in the 'yaml' property within 'definition'
                          definition_yaml = definition["yaml"]
                          parsed_yaml = yaml.safe_load(definition_yaml)
                          repo_name = parsed_yaml.get("repository", {}).get("name")

                          # Check if repository name starts with the prefix
                          if repo_name and repo_name.startswith(repo_prefix):
                              pipeline_info = {
                                  "name": pipeline["name"],
                                  "id": pipeline["id"],
                                  "repository": repo_name,
                                  "owner": definition_data.get("createdBy", {}).get("displayName"),
                              }
                              pipelines.append(pipeline_info)
                              print(f"Pipeline: {pipeline['name']}, Owner: {pipeline_info['owner']}, Repository: {pipeline_info['repository']}")
                      except yaml.YAMLError as ex:
                          print(f"Error parsing YAML definition for pipeline {pipeline['id']}: {ex}")
          else:
              print(f"Error retrieving pipelines: {response.status_code}")

      # Retrieve parameters from pipeline configuration
      organization_url = parameters.organizationUrl
      personal_access_token = parameters.personalAccessToken  # Access token retrieved securely
      project_name = parameters.projectName
      repo_prefix = "ab9180"

      get_pipelines_and_ownership(organization_url, personal_access_token, project_name, repo_prefix)





===============================================================================================
import requests
from requests.auth import HTTPBasicAuth
import json
import os

# Replace these values with your Azure DevOps details
organization = os.environ['organization']
project = os.environ['project']
pat = os.environ['AZURE_DEVOPS_EXT_PAT']  # Using environment variable for security
repo_prefix = os.environ['repo_prefix']  # The first 6 letters prefix for your repos

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
with open('pipelines_info.json', '
w') as f:
    json.dump(pipelines_info, f, indent=2)

# Print the result for logging purposes
for info in pipelines_info:
    print(f"Pipeline: {info['Pipeline Name']}, Owner: {info['Owner']}")
