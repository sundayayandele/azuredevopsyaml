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
