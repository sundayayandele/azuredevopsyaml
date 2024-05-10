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
