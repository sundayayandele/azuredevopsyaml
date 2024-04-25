import yaml
from atlassian import Confluence
import os

def read_md_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def create_or_update_confluence_page(confluence, space_key, parent_page_title, title, content):
    parent_page = confluence.get_page_by_title(space_key, parent_page_title)
    if not parent_page:
        raise Exception(f"Parent page '{parent_page_title}' not found in space '{space_key}'")
    
    page = confluence.get_page_by_title(space_key, title)
    if page:
        confluence.update_page(page['id'], title, content, minor_edit=False)
        print("Page updated successfully:", page['id'])
    else:
        page_data = {
            'type': 'page',
            'title': title,
            'space': {'key': space_key},
            'ancestors': [{'id': parent_page['id']}],
            'body': {
                'storage': {
                    'value': content,
                    'representation': 'storage'
                }
            }
        }
        page_creation_response = confluence.create_content(content=page_data)
        print("Page created successfully:", page_creation_response['id'])

def main():
    # Load YAML configuration
    with open('call_script.yaml', 'r') as yaml_file:
        config = yaml.safe_load(yaml_file)

    # Define Confluence connection using API token
    confluence = Confluence(
        url=config['confluence_url'],
        token=config['confluence_token']
    )

    # Read content from Azure repo file
    md_content = read_md_file(config['azure_repo_file_path'])

    # Define Confluence page details
    space_key = config['confluence_space_key']
    parent_page_title = config['confluence_parent_page_title']
    page_title = config['confluence_page_title']

    # Create or update the Confluence page
    create_or_update_confluence_page(confluence, space_key, parent_page_title, page_title, md_content)

if __name__ == "__main__":
    main()
