#Script 2: Python Script (copy_azure_to_confluence.py)

import yaml
from atlassian import Confluence
import os

def read_md_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

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
    # Load YAML configuration
    with open('call_script.yaml', 'r') as yaml_file:
        config = yaml.safe_load(yaml_file)

    # Define Confluence connection
    confluence = Confluence(
        url=config['confluence_url'],
        username=config['confluence_username'],
        password=config['confluence_password']
    )

    # Read content from Azure repo file
    md_content = read_md_file(config['azure_repo_file_path'])

    # Define Confluence page details
    space_key = config['confluence_space_key']
    parent_page_id = config['confluence_parent_page_id']
    page_title = config['confluence_page_title']

    # Check if the page already exists, if so, delete it
    existing_page = confluence.get_page_by_title(space_key, page_title)
    if existing_page:
        confluence.remove_page(existing_page['id'])

    # Create the Confluence page
    page_creation_response = create_confluence_page(confluence, space_key, parent_page_id, page_title, md_content)
    print("Page created successfully:", page_creation_response['id'])

if __name__ == "__main__":
    main()
