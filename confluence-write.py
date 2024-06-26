def get_all_pages_under_parent(parent_title, confluence, space_key):
    all_pages = []

    # Function to recursively fetch pages
    def fetch_pages_recursive(parent_id):
        pages = confluence.get_child_pages(page_id=parent_id, start=0, limit=1000)  # Adjust limit as needed
        for page in pages['page']:
            all_pages.append(page)
            fetch_pages_recursive(page['id'])

    # Get parent page ID
    parent_page = confluence.get_page_by_title(space=space_key, title=parent_title)
    if not parent_page:
        print(f"Parent page '{parent_title}' not found.")
        return []

    fetch_pages_recursive(parent_page[0]['id'])
    return all_pages



=========================================================
def get_all_pages_under_parent(parent_title, confluence, space_key):
    all_pages = []

    # Function to recursively fetch pages
    def fetch_pages_recursive(title):
        pages = confluence.get_page_by_title(space=space_key, title=title)
        for page in pages:
            all_pages.append(page)
            # Check if the page has child pages based on any metadata or relationships
            # For example, you might need to check for labels, attachments, or links to other pages
            # Then call this function recursively for each child page
            # Example: fetch_pages_recursive(page['title'])

    fetch_pages_recursive(parent_title)
    return all_pages
==========================================================

from atlassian import Confluence

# Function to fetch all Confluence page titles and subpage titles under a parent page
def get_all_confluence_page_titles(parent_page_title, confluence):
    # Fetch page data
    page_data = confluence.get_page_by_title(space='SPACE_KEY', title=parent_page_title)
    
    # Initialize list to store page titles
    all_page_titles = []
    
    # Function to recursively get all subpage titles
    def get_subpages(page_data):
        all_page_titles.append(page_data['title'])  # Add current page title
        
        # Fetch children pages recursively
        for child in page_data['children']['page']:
            child_page_data = confluence.get_page_by_id(child['id'])
            get_subpages(child_page_data)
    
    # Start recursively fetching subpage titles
    get_subpages(page_data)
    
    return all_page_titles

# Function to move Confluence page to 'Archive' if not found in Azure DevOps repo
def move_to_archive(confluence_page_title, confluence):
    # Move Confluence page to 'Archive' space
    archive_space_key = 'ARCHIVE_SPACE_KEY'
    archive_parent_page_title = 'ARCHIVE_PARENT_PAGE_TITLE'
    archive_page = confluence.get_page_by_title(space=archive_space_key, title=archive_parent_page_title)
    
    # Update page parent to move it to 'Archive'
    confluence.update_page(
        page_id=confluence_page_title['id'],
        title=confluence_page_title['title'],
        body=confluence_page_title['body'],
        space=archive_space_key,
        parent_id=archive_page['id']
    )
    print(f"Confluence page '{confluence_page_title['title']}' moved to 'Archive'")

# Main function
def main():
    confluence_token = 'YOUR_CONFLUENCE_TOKEN'  # Replace with your Confluence API token
    confluence = Confluence(url='YOUR_CONFLUENCE_URL', username='USERNAME', password='PASSWORD', token=confluence_token)
    
    parent_page_title = 'YOUR_CONFLUENCE_PARENT_PAGE_TITLE'  # Replace with actual parent page title
    
    # Fetch all Confluence page titles and subpage titles under the parent page
    all_confluence_page_titles = get_all_confluence_page_titles(parent_page_title, confluence)
    
    # Azure DevOps repo folder paths
    azure_repo_folder_paths = [
        'opts/vsts_agent/_work/1/s/07. Platform/07.07 wow/07.07.03 bag.md',
        'opts/vsts_agent/_work/1/s/07. Platform/07.06 repositories/07.06.07 report auto/report.md',
        'opts/vsts_agent/_work/1/s/07. Platform/07.05 monitor and repot/07.05.01 healthcheck/health.md'
    ]
    
    # Compare Confluence page titles with Azure DevOps repo folder paths
    for page_title in all_confluence_page_titles:
        if not any(page_title in folder_path for folder_path in azure_repo_folder_paths):
            move_to_archive(page_title, confluence)

if __name__ == "__main__":
    main()



===========================================================================================================================
import requests

# Function to fetch all Confluence page titles and subpage titles under a parent page
def get_all_confluence_page_titles(parent_page_title):
    # Make API request to fetch page data
    # Replace 'YOUR_CONFLUENCE_API_ENDPOINT' and 'YOUR_CONFLUENCE_AUTHORIZATION_HEADER' with actual values
    response = requests.get(
        f'YOUR_CONFLUENCE_API_ENDPOINT/content?title={parent_page_title}',
        headers={'Authorization': 'YOUR_CONFLUENCE_AUTHORIZATION_HEADER'}
    )
    
    # Extract page data from the response
    page_data = response.json()['results'][0]
    
    # Initialize list to store page titles
    all_page_titles = []
    
    # Function to recursively get all subpage titles
    def get_subpages(page_data):
        all_page_titles.append(page_data['title'])  # Add current page title
        
        # Check if the current page has children (subpages)
        if 'children' in page_data['_links']:
            # Fetch children pages recursively
            for child_link in page_data['_links']['children']:
                child_response = requests.get(child_link['href'], headers={'Authorization': 'YOUR_CONFLUENCE_AUTHORIZATION_HEADER'})
                child_page_data = child_response.json()
                get_subpages(child_page_data)
    
    # Start recursively fetching subpage titles
    get_subpages(page_data)
    
    return all_page_titles

# Function to fetch Azure DevOps repo folder names
def get_azure_repo_folder_names():
    # Make API request to fetch folder names from Azure DevOps repo
    # Replace 'YOUR_AZURE_DEVOPS_ORGANIZATION', 'YOUR_AZURE_DEVOPS_PROJECT', and 'YOUR_AZURE_DEVOPS_REPO' with actual values
    response = requests.get(
        f'https://dev.azure.com/YOUR_AZURE_DEVOPS_ORGANIZATION/YOUR_AZURE_DEVOPS_PROJECT/_apis/git/repositories/YOUR_AZURE_DEVOPS_REPO/items?scopePath=/&api-version=6.0',
        headers={'Authorization': 'YOUR_AZURE_DEVOPS_AUTHORIZATION_HEADER'}
    )
    
    # Extract folder names from the response
    folder_names = [item['path'] for item in response.json()['value'] if item['gitObjectType'] == 'tree']
    
    return folder_names

# Function to move Confluence page to 'Archive' if not found in Azure DevOps repo
def move_to_archive(parent_page_title, confluence_page_title):
    # Make API request to move Confluence page to 'Archive'
    # Replace 'YOUR_CONFLUENCE_API_ENDPOINT' and 'YOUR_CONFLUENCE_AUTHORIZATION_HEADER' with actual values
    payload = {
        "ancestors": [{"type": "page", "id": "ARCHIVE_PARENT_PAGE_ID"}]  # Replace 'ARCHIVE_PARENT_PAGE_ID' with the actual ID of the 'Archive' page
    }
    response = requests.put(
        f'YOUR_CONFLUENCE_API_ENDPOINT/content/{confluence_page_id}',
        headers={'Authorization': 'YOUR_CONFLUENCE_AUTHORIZATION_HEADER'},
        json=payload
    )
    
    if response.status_code == 204:
        print(f"Confluence page '{confluence_page_title}' moved to 'Archive'")
    else:
        print(f"Failed to move Confluence page '{confluence_page_title}' to 'Archive'")

# Main function
def main():
    parent_page_title = 'YOUR_CONFLUENCE_PARENT_PAGE_TITLE'  # Replace with actual parent page title
    target_title = 'Archive'
    
    # Fetch all Confluence page titles and subpage titles under the parent page
    all_confluence_page_titles = get_all_confluence_page_titles(parent_page_title)
    
    # Fetch Azure DevOps repo folder names
    azure_repo_folder_names = get_azure_repo_folder_names()
    
    # Compare Confluence page titles with Azure DevOps repo folder names
    for page_title in all_confluence_page_titles:
        if page_title not in azure_repo_folder_names:
            move_to_archive(parent_page_title, page_title)

if __name__ == "__main__":
    main()

=======================================================================
import requests

# Function to fetch Confluence page titles under a particular parent page
def get_confluence_page_titles(parent_page_title):
    # Make API request to fetch page titles under the parent page
    # Replace 'YOUR_CONFLUENCE_API_ENDPOINT' and 'YOUR_CONFLUENCE_AUTHORIZATION_HEADER' with actual values
    response = requests.get(
        f'YOUR_CONFLUENCE_API_ENDPOINT/content?title={parent_page_title}',
        headers={'Authorization': 'YOUR_CONFLUENCE_AUTHORIZATION_HEADER'}
    )
    
    # Extract page titles from the response
    page_titles = [page['title'] for page in response.json()['results']]
    
    return page_titles

# Function to fetch Azure DevOps repo folder names
def get_azure_repo_folder_names():
    # Make API request to fetch folder names from Azure DevOps repo
    # Replace 'YOUR_AZURE_DEVOPS_ORGANIZATION', 'YOUR_AZURE_DEVOPS_PROJECT', and 'YOUR_AZURE_DEVOPS_REPO' with actual values
    response = requests.get(
        f'https://dev.azure.com/YOUR_AZURE_DEVOPS_ORGANIZATION/YOUR_AZURE_DEVOPS_PROJECT/_apis/git/repositories/YOUR_AZURE_DEVOPS_REPO/items?scopePath=/&api-version=6.0',
        headers={'Authorization': 'YOUR_AZURE_DEVOPS_AUTHORIZATION_HEADER'}
    )
    
    # Extract folder names from the response
    folder_names = [item['path'] for item in response.json()['value'] if item['gitObjectType'] == 'tree']
    
    return folder_names

# Function to move Confluence page to 'Archive' if not found in Azure DevOps repo
def move_to_archive(parent_page_title, confluence_page_title):
    # Make API request to move Confluence page to 'Archive'
    # Replace 'YOUR_CONFLUENCE_API_ENDPOINT' and 'YOUR_CONFLUENCE_AUTHORIZATION_HEADER' with actual values
    payload = {
        "ancestors": [{"type": "page", "id": "ARCHIVE_PARENT_PAGE_ID"}]  # Replace 'ARCHIVE_PARENT_PAGE_ID' with the actual ID of the 'Archive' page
    }
    response = requests.put(
        f'YOUR_CONFLUENCE_API_ENDPOINT/content/{confluence_page_id}',
        headers={'Authorization': 'YOUR_CONFLUENCE_AUTHORIZATION_HEADER'},
        json=payload
    )
    
    if response.status_code == 204:
        print(f"Confluence page '{confluence_page_title}' moved to 'Archive'")
    else:
        print(f"Failed to move Confluence page '{confluence_page_title}' to 'Archive'")

# Main function
def main():
    parent_page_title = 'YOUR_CONFLUENCE_PARENT_PAGE_TITLE'  # Replace with actual parent page title
    target_title = 'Archive'
    
    # Fetch Confluence page titles under the parent page
    confluence_page_titles = get_confluence_page_titles(parent_page_title)
    
    # Fetch Azure DevOps repo folder names
    azure_repo_folder_names = get_azure_repo_folder_names()
    
    # Compare Confluence page titles with Azure DevOps repo folder names
    for page_title in confluence_page_titles:
        if page_title not in azure_repo_folder_names:
            move_to_archive(parent_page_title, page_title)

if __name__ == "__main__":
    main()


==========================================
import requests
import base64
from requests.auth import HTTPBasicAuth

# Confluence credentials and API endpoint
CONFLUENCE_URL = "https://your-confluence-url.com/rest/api/content"
CONFLUENCE_USERNAME = "your_confluence_username"
CONFLUENCE_PASSWORD = "your_confluence_password"

# Azure Repo credentials and API endpoint
AZURE_ORG = "your_azure_organization"
AZURE_PROJECT = "your_azure_project"
REPO_NAME = "your_azure_repo_name"
FILE_PATH = "path/to/your/file/in/repo"
AZURE_TOKEN = "your_azure_personal_access_token"

def create_confluence_page(title, content):
    auth = HTTPBasicAuth(CONFLUENCE_USERNAME, CONFLUENCE_PASSWORD)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "type": "page",
        "title": title,
        "space": {"key": "SPACEKEY"},  # Replace "SPACEKEY" with your space key
        "body": {
            "storage": {
                "value": content,
                "representation": "storage"
            }
        }
    }
    response = requests.post(CONFLUENCE_URL, json=data, headers=headers, auth=auth)
    if response.status_code == 200:
        print("Confluence page created successfully!")
        return response.json()["id"]
    else:
        print("Error creating Confluence page:", response.text)
        return None

def get_file_content_from_azure():
    url = f"https://dev.azure.com/{AZURE_ORG}/{AZURE_PROJECT}/_apis/git/repositories/{REPO_NAME}/items?path={FILE_PATH}&api-version=6.0"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f':{AZURE_TOKEN}'.encode()).decode()}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["content"]
    else:
        print("Error fetching file content from Azure Repo:", response.text)
        return None

def main():
    # Fetch file content from Azure Repo
    file_content = get_file_content_from_azure()
    if file_content is None:
        return

    # Create Confluence page with the fetched content
    title = "Your Confluence Page Title"
    page_content = file_content.decode("utf-8")  # Assuming file content is in UTF-8 encoding
    page_id = create_confluence_page(title, page_content)
    if page_id:
        print("Confluence page ID:", page_id)

if __name__ == "__main__":
    main()
