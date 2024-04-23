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
