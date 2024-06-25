import subprocess
import json
import os

# Function to execute an az command and return the output
def az_cli(command):
    result = subprocess.run(['az'] + command.split(), capture_output=True, text=True)
    if result.returncode != 0:
        print(f'Error running command: az {command}')
        print(result.stderr)
        return None
    return json.loads(result.stdout)

# Function to list repositories in the project
def list_repos():
    command = f'devops repo list --organization https://dev.azure.com/SAAM --project Abc --query "[].name"'
    return az_cli(command)

# Function to list items in a repo path
def list_repo_items(repo_name, path):
    command = f'devops repo list --organization https://dev.azure.com/SAAM --project Abc --repository {repo_name} --path {path} --query "[].path"'
    return az_cli(command)

# List all repos in the project
repos = list_repos()
if not repos:
    print("No repositories found.")
    exit(1)

yaml_files = []

# Iterate over each repo and look for 'pipeline' folder
for repo in repos:
    items = list_repo_items(repo, '/pipeline')
    if items:
        for item in items:
            if item.endswith('.yaml') or item.endswith('.yml'):
                yaml_files.append({'repo': repo, 'file': item})

# Save the result to a JSON file
with open('yaml_files.json', 'w') as f:
    json.dump(yaml_files, f, indent=2)

# Print the result for logging purposes
for file in yaml_files:
    print(f"Repository: {file['repo']}, File: {file['file']}")
