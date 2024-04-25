import yaml
from atlassian import Confluence
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

def read_yaml_file(file_path):
    with open(file_path, 'r') as yaml_file:
        return yaml.safe_load(yaml_file)

def read_azure_repo_file(repo_name, pat, file_path):
    credentials = BasicAuthentication('', pat)
    connection = Connection(base_url=f'https://dev.azure.com/{repo_name}', creds=credentials)
    repo_client = connection.clients.get_git_client()
    item_content = repo_client.get_item_text(repo_name, file_path, 'main')
    return item_content

def create_confluence_page(confluence, space_key, parent_page_id, title, content):
    page_data = {
        'type': 'page',
        'title': title,
        'space': {'key': space_key},
        'ancestors': [{'id': parent_page_id}],
        'body': {
            'storage': {
                'value': content,
                'representation': 'storage'
            }
        }
    }
    return confluence.create_content(content=page_data)

def main():
    # Read task details from YAML file
    task_details = read_yaml_file('confluence_task.yaml')

    # Read content from Azure repo file
    azure_content = read_azure_repo_file(task_details['azure_repo_name'], task_details['azure_pat'], task_details['repo_file_path'])

    # Connect to Confluence
    confluence = Confluence(
        url=task_details['confluence_url'],
        username=task_details['confluence_username'],
        password=task_details['confluence_password']
    )

    # Create the Confluence page
    page_creation_response = create_confluence_page(confluence, task_details['space_key'], task_details['parent_page_id'], task_details['confluence_page_title'], azure_content)
    print("Page created successfully:", page_creation_response['id'])

if __name__ == "__main__":
    main()
