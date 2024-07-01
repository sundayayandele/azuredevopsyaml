Here's a Python snippet that can convert both JSON and HTML data to Markdown tables:

Python
import json
from bs4 import BeautifulSoup  # For HTML parsing

def json_to_markdown_table(json_data):
  """
  Converts a JSON object to a Markdown table.

  Args:
      json_data: The JSON data as a dictionary or list.

  Returns:
      A string containing the Markdown table representation of the JSON data.
  """
  headers = list(json_data[0].keys())  # Get headers from the first object
  table_rows = []

  for item in json_data:
    row_data = [str(item[header]) for header in headers]
    table_rows.append(row_data)

  # Construct the Markdown table
  table_str = "| " + " | ".join(headers) + " |\n"
  table_str += "|-" * (len(headers) * 2 + 1) + "|\n"
  for row in table_rows:
    table_str += "| " + " | ".join(row) + " |\n"

  return table_str

def html_to_markdown_table(html_data):
  """
  Converts an HTML table to a Markdown table.

  Args:
      html_data: The HTML content as a string.

  Returns:
      A string containing the Markdown table representation of the HTML table, 
      or None if no table is found.
  """
  soup = BeautifulSoup(html_data, 'html.parser')
  table = soup.find('table')  # Find the first table element

  if table:
    headers = [th.text.strip() for th in table.find_all('th')]  # Extract headers
    table_rows = []

    for row in table.find_all('tr')[1:]:  # Skip header row
      row_data = [td.text.strip() for td in row.find_all('td')]
      table_rows.append(row_data)

    # Construct the Markdown table (similar to json_to_markdown_table)
    table_str = "| " + " | ".join(headers) + " |\n"
    table_str += "|-" * (len(headers) * 2 + 1) + "|\n"
    for row in table_rows:
      table_str += "| " + " | ".join(row) + " |\n"

    return table_str
  else:
    return None

# Example Usage
# Assuming your JSON data is loaded into a variable called 'data'
json_table = json_to_markdown_table(data)

# Assuming your HTML data is loaded into a variable called 'html_content'
html_table = html_to_markdown_table(html_content)

# Print or write the converted Markdown tables
if json_table:
  print("Markdown table from JSON:")
  print(json_table)

if html_table:
  print("Markdown table from HTML:")
  print(html_table)
  

-------------------------------------------------------------------------------------------------------------
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
        response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)
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
        response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)
        memberships = response.json()
        if 'value' in memberships:
            return [membership['displayName'] for membership in memberships['value']]
        else:
            print(f"No memberships found for user descriptor: {user_descriptor}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving user memberships: {e}")
        return []

if __name__ == "__main__":
    organization = 'SAAM'
    display_name = 'John Doe'  # Replace with the display name of the user you want to query

    user_descriptor = get_user_descriptor(display_name, organization)
    if user_descriptor:
        memberships = get_user_memberships(user_descriptor, organization)
        print(f"User Descriptor: {user_descriptor}")
        print(f"Memberships: {', '.join(memberships)}")
    else:
        print(f"User '{display_name}' not found or has no entitlements/memberships.")



============================================================================================
import json
import os
import subprocess

def run_az_cli_command(command):
    """Run an Azure CLI command and return the result as a dictionary."""
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error running command {command}: {stderr.decode('utf-8')}")
        return None
    try:
        return json.loads(stdout.decode('utf-8'))
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return None

def az_devops_login(organization, project):
    """Login to Azure DevOps using a service principal."""
    client_id = os.getenv('AZURE_CLIENT_ID')
    client_secret = os.getenv('AZURE_CLIENT_SECRET')
    tenant_id = os.getenv('AZURE_TENANT_ID')

    command = f"az login --service-principal -u {client_id} -p {client_secret} --tenant {tenant_id}"
    login_result = run_az_cli_command(command)
    if login_result is None:
        print("Failed to login to Azure CLI")
        return False

    command = f"az devops configure --defaults organization=https://dev.azure.com/{organization} project={project}"
    configure_result = run_az_cli_command(command)
    if configure_result is None:
        print("Failed to configure Azure DevOps defaults")
        return False

    return True

def get_pipelines_from_folder(organization, project, folder_path):
    """Get all pipelines from a specific folder."""
    token = os.getenv('SYSTEM_ACCESSTOKEN')
    command = f"az pipelines list --organization https://dev.azure.com/{organization} --project {project} --folder-path '{folder_path}' --output json --only-show-errors --token {token}"
    return run_az_cli_command(command)

def get_pipeline_details(organization, project, pipeline_id):
    """Get details of a specific pipeline."""
    token = os.getenv('SYSTEM_ACCESSTOKEN')
    command = f"az pipelines show --organization https://dev.azure.com/{organization} --project {project} --id {pipeline_id} --output json --only-show-errors --token {token}"
    return run_az_cli_command(command)

def get_user_descriptor(user_id, organization):
    """Get the user descriptor using user entitlements API."""
    token = os.getenv('SYSTEM_ACCESSTOKEN')
    command = f"az rest --method get --uri https://vsaex.dev.azure.com/{organization}/_apis/userentitlements?api-version=7.1-preview-3 --token {token}"
    result = run_az_cli_command(command)
    if result:
        for entitlement in result.get('value', []):
            user = entitlement.get('user', {})
            if user.get('id') == user_id:
                return entitlement.get('descriptor')
    return None

def get_user_memberships(user_descriptor, organization):
    """Get user memberships using the user descriptor."""
    token = os.getenv('SYSTEM_ACCESSTOKEN')
    command = f"az devops security group list --organization https://dev.azure.com/{organization} --query '[?members[?member.displayName==`{user_descriptor}`]].{displayName: displayName}' --output json --token {token}"
    memberships = run_az_cli_command(command)
    if memberships:
        return [membership['displayName'] for membership in memberships]
    return []

def find_pipeline_details(organization, project, folder_paths):
    """Get pipeline details from the specified folders."""
    pipeline_details = []

    for folder_path in folder_paths:
        pipelines = get_pipelines_from_folder(organization, project, folder_path)
        if pipelines is None:
            print(f"No pipelines found for folder: {folder_path}")
            continue

        for pipeline in pipelines:
            pipeline_id = pipeline['id']
            details = get_pipeline_details(organization, project, pipeline_id)
            if details:
                pipeline_name = details['name']
                repository_name = details.get('repository', {}).get('name', 'Unknown')
                author_name = details.get('authoredBy', {}).get('displayName', 'Unknown')
                author_id = details.get('authoredBy', {}).get('id', None)
                if author_id:
                    author_descriptor = get_user_descriptor(author_id, organization)
                    if author_descriptor:
                        author_memberships = get_user_memberships(author_descriptor, organization)
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

    return pipeline_details

if __name__ == "__main__":
    organization = 'SAAM'
    project = 'Abc'
    folder_filters = ['\\S0123\\abc', '\\S0123\\def', '\\S0123\\aba', '\\S0123\\riso', '\\S0123\\ahs', '\\S0123\\eid']

    if az_devops_login(organization, project):
        pipeline_details = find_pipeline_details(organization, project, folder_filters)

        with open('pipeline_details.json', 'w') as f:
            json.dump(pipeline_details, f, indent=2)

        for detail in pipeline_details:
            print(f"Pipeline Name: {detail['Pipeline Name']}, Repository Name: {detail['Repository Name']}, Author: {detail['Author']}, Author Memberships: {', '.join(detail['Author Memberships'])}")
    else:
        print("Azure DevOps login failed.")




====================================
import json
import os
import subprocess

def run_az_cli_command(command):
    """Run an Azure CLI command and return the result as a dictionary."""
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error running command {command}: {stderr.decode('utf-8')}")
        return None
    try:
        return json.loads(stdout.decode('utf-8'))
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return None

def az_devops_login(organization, project):
    """Login to Azure DevOps using a service principal."""
    client_id = os.getenv('AZURE_CLIENT_ID')
    client_secret = os.getenv('AZURE_CLIENT_SECRET')
    tenant_id = os.getenv('AZURE_TENANT_ID')

    command = f"az login --service-principal -u {client_id} -p {client_secret} --tenant {tenant_id}"
    login_result = run_az_cli_command(command)
    if login_result is None:
        print("Failed to login to Azure CLI")
        return False

    command = f"az devops configure --defaults organization=https://dev.azure.com/{organization} project={project}"
    configure_result = run_az_cli_command(command)
    if configure_result is None:
        print("Failed to configure Azure DevOps defaults")
        return False

    return True

def get_pipelines_from_folder(organization, project, folder_path):
    """Get all pipelines from a specific folder."""
    command = f"az devops pipeline list --organization https://dev.azure.com/{organization} --project {project} --folder-path '{folder_path}' --output json --only-show-errors"
    return run_az_cli_command(command)

def get_pipeline_details(organization, project, pipeline_id):
    """Get details of a specific pipeline."""
    command = f"az devops pipeline show --organization https://dev.azure.com/{organization} --project {project} --id {pipeline_id} --output json --only-show-errors"
    return run_az_cli_command(command)

def get_user_descriptor(user_id, organization):
    """Get the user descriptor using user entitlements API."""
    command = f"az rest --method get --uri https://vsaex.dev.azure.com/{organization}/_apis/userentitlements?api-version=7.1-preview-3"
    result = run_az_cli_command(command)
    if result:
        for entitlement in result.get('value', []):
            user = entitlement.get('user', {})
            if user.get('id') == user_id:
                return entitlement.get('descriptor')
    return None

def get_user_memberships(user_descriptor, organization):
    """Get user memberships using the user descriptor."""
    command = f"az devops security group list --organization https://dev.azure.com/{organization} --query '[?members[?member.displayName==`{user_descriptor}`]].{displayName: displayName}' --output json"
    memberships = run_az_cli_command(command)
    if memberships:
        return [membership['displayName'] for membership in memberships]
    return []

def find_pipeline_details(organization, project, folder_paths):
    """Get pipeline details from the specified folders."""
    pipeline_details = []

    for folder_path in folder_paths:
        pipelines = get_pipelines_from_folder(organization, project, folder_path)
        if pipelines is None:
            print(f"No pipelines found for folder: {folder_path}")
            continue

        for pipeline in pipelines:
            pipeline_id = pipeline['id']
            details = get_pipeline_details(organization, project, pipeline_id)
            if details:
                pipeline_name = details['name']
                repository_name = details.get('repository', {}).get('name', 'Unknown')
                author_name = details.get('authoredBy', {}).get('displayName', 'Unknown')
                author_id = details.get('authoredBy', {}).get('id', None)
                if author_id:
                    author_descriptor = get_user_descriptor(author_id, organization)
                    if author_descriptor:
                        author_memberships = get_user_memberships(author_descriptor, organization)
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

    return pipeline_details

if __name__ == "__main__":
    organization = 'SAAM'
    project = 'Abc'
    folder_filters = ['\\S0123\\abc', '\\S0123\\def', '\\S0123\\aba', '\\S0123\\riso', '\\S0123\\ahs', '\\S0123\\eid']

    if az_devops_login(organization, project):
        pipeline_details = find_pipeline_details(organization, project, folder_filters)

        with open('pipeline_details.json', 'w') as f:
            json.dump(pipeline_details, f, indent=2)

        for detail in pipeline_details:
            print(f"Pipeline Name: {detail['Pipeline Name']}, Repository Name: {detail['Repository Name']}, Author: {detail['Author']}, Author Memberships: {', '.join(detail['Author Memberships'])}")
    else:
        print("Azure DevOps login failed.")




======================================================================
import json
import os
import subprocess

def run_az_cli_command(command):
    """Run an Azure CLI command and return the result as a dictionary."""
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error running command {command}: {stderr.decode('utf-8')}")
        return None
    return json.loads(stdout.decode('utf-8'))

def get_pipelines_from_folder(organization, project, folder_path, token):
    """Get all pipelines from a specific folder."""
    command = f"az devops pipeline list --organization https://dev.azure.com/{organization} --project {project} --folder-path '{folder_path}' --output json --only-show-errors"
    return run_az_cli_command(command)

def get_pipeline_details(organization, project, pipeline_id, token):
    """Get details of a specific pipeline."""
    command = f"az devops pipeline show --organization https://dev.azure.com/{organization} --project {project} --id {pipeline_id} --output json --only-show-errors"
    return run_az_cli_command(command)

def get_user_descriptor(user_id, organization):
    """Get the user descriptor using user entitlements API."""
    command = f"az rest --method get --uri https://vsaex.dev.azure.com/{organization}/_apis/userentitlements?api-version=7.1-preview-3"
    result = run_az_cli_command(command)
    if result:
        for entitlement in result.get('value', []):
            user = entitlement.get('user', {})
            if user.get('id') == user_id:
                return entitlement.get('descriptor')
    return None

def get_user_memberships(user_descriptor, organization):
    """Get user memberships using the user descriptor."""
    command = f"az devops security group list --organization https://dev.azure.com/{organization} --query '[?members[?member.displayName==`{user_descriptor}`]].{displayName: displayName}' --output json"
    memberships = run_az_cli_command(command)
    if memberships:
        return [membership['displayName'] for membership in memberships]
    return []

def find_pipeline_details_recursively(organization, project, folder_paths, token):
    """Recursively get pipeline details from a folder and its subfolders."""
    pipeline_details = []

    def traverse_folders(current_folder):
        pipelines = get_pipelines_from_folder(organization, project, current_folder, token)
        
        for pipeline in pipelines:
            pipeline_id = pipeline['id']
            details = get_pipeline_details(organization, project, pipeline_id, token)
            if details:
                pipeline_name = details['name']
                repository_name = details.get('repository', {}).get('name', 'Unknown')
                author_name = details.get('authoredBy', {}).get('displayName', 'Unknown')
                author_id = details.get('authoredBy', {}).get('id', None)
                if author_id:
                    author_descriptor = get_user_descriptor(author_id, organization)
                    if author_descriptor:
                        author_memberships = get_user_memberships(author_descriptor, organization)
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
        subfolders_command = f"az devops pipeline list-folders --organization https://dev.azure.com/{organization} --project {project} --folder-path '{current_folder}' --output json --only-show-errors"
        subfolders = run_az_cli_command(subfolders_command)
        if subfolders:
            for subfolder in subfolders:
                traverse_folders(subfolder['path'])

    for folder_path in folder_paths:
        traverse_folders(folder_path)
    
    return pipeline_details

if __name__ == "__main__":
    organization = 'SAAM'
    project = 'Abc'
    folder_filters = ['\\S0123\\abc', '\\S0123\\def', '\\S0123\\aba', '\\S0123\\riso', '\\S0123\\ahs', '\\S0123\\eid']
    token = os.getenv('SYSTEM_ACCESSTOKEN')

    pipeline_details = find_pipeline_details_recursively(organization, project, folder_filters, token)

    with open('pipeline_details.json', 'w') as f:
        json.dump(pipeline_details, f, indent=2)

    for detail in pipeline_details:
        print(f"Pipeline Name: {detail['Pipeline Name']}, Repository Name: {detail['Repository Name']}, Author: {detail['Author']}, Author Memberships: {', '.join(detail['Author Memberships'])}")
