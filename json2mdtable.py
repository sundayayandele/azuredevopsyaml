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
    python -m pip install requests
  displayName: 'Install dependencies'

- script: |
    python get_pipeline_details.py
  displayName: 'Get Pipeline Details'
  env:
    SYSTEM_ACCESSTOKEN: $(System.AccessToken)

- script: |
    sudo apt-get update
    sudo apt-get install -y jq
    sudo wget https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64 -O /usr/bin/yq
    sudo chmod +x /usr/bin/yq
  displayName: 'Install jq and yq'

- script: |
    jq -r '["Pipeline Name", "Repository Name", "YAML File Name", "Author", "Author Memberships"], (.[] | [.["Pipeline Name"], .["Repository Name"], .["YAML File Name"], .["Author"], (.["Author Memberships"] | join(", "))]) | @csv' pipeline_details.json > pipeline_details.csv

    yq eval -P '. | 
    "## Pipeline Details\n" + 
    "| Pipeline Name | Repository Name | YAML File Name | Author | Author Memberships |\n| ------------- | --------------- | -------------- | ------ | ------------------ |\n" +
    (.[] | "| " + .["Pipeline Name"] + " | " + .["Repository Name"] + " | " + .["YAML File Name"] + " | " + .["Author"] + " | " + (.["Author Memberships"] | join(", ")) + " |\n")' pipeline_details.json > pipeline_details.md
  displayName: 'Convert JSON to CSV and Markdown'

- publish: pipeline_details.csv
  artifact: pipeline-details-csv
  displayName: 'Publish Pipeline Details CSV'

- publish: pipeline_details.md
  artifact: pipeline-details-markdown
  displayName: 'Publish Pipeline Details Markdown'

========================================================
import json
import pandas as pd

def generate_json():
    # Example data to be saved in JSON
    pipeline_details = [
        {
            "Pipeline Name": "Pipeline1",
            "Repository Name": "Repo1",
            "Author": "Author1",
            "Author Memberships": ["Group1", "Group2"],
            "Team Memberships": ["Team1", "Team2"]
        },
        {
            "Pipeline Name": "Pipeline2",
            "Repository Name": "Repo2",
            "Author": "Author2",
            "Author Memberships": ["Group3"],
            "Team Memberships": ["Team3"]
        }
    ]

    # Save to JSON file
    with open('pipeline_details.json', 'w') as f:
        json.dump(pipeline_details, f, indent=2)

def json_to_md():
    # Load data from JSON file
    with open('pipeline_details.json', 'r') as f:
        data = json.load(f)

    # Normalize the data to flatten lists into comma-separated strings
    for item in data:
        item['Author Memberships'] = ', '.join(item['Author Memberships'])
        item['Team Memberships'] = ', '.join(item['Team Memberships'])

    # Convert data to DataFrame
    df = pd.DataFrame(data)

    # Convert DataFrame to Markdown table
    md_table = df.to_markdown(index=False)

    # Save to Markdown file
    with open('pipeline_details.md', 'w') as f:
        f.write(md_table)

    # Print the Markdown table for logging purposes
    print(md_table)

# Execute functions sequentially
generate_json()
json_to_md()



==================================
import json
import pandas as pd

def generate_json():
    # Example data to be saved in JSON
    pipeline_details = [
        {
            "Pipeline Name": "Pipeline1",
            "Repository Name": "Repo1",
            "Author": "Author1",
            "Author Memberships": ["Group1", "Group2"],
            "Team Memberships": ["Team1", "Team2"]
        },
        {
            "Pipeline Name": "Pipeline2",
            "Repository Name": "Repo2",
            "Author": "Author2",
            "Author Memberships": ["Group3"],
            "Team Memberships": ["Team3"]
        }
    ]

    # Save to JSON file
    with open('pipeline_details.json', 'w') as f:
        json.dump(pipeline_details, f, indent=2)

def json_to_md():
    # Load data from JSON file
    with open('pipeline_details.json', 'r') as f:
        data = json.load(f)

    # Normalize the data to flatten lists into comma-separated strings
    for item in data:
        item['Author Memberships'] = ', '.join(item['Author Memberships'])
        item['Team Memberships'] = ', '.join(item['Team Memberships'])

    # Convert data to DataFrame
    df = pd.DataFrame(data)

    # Convert DataFrame to Markdown table
    md_table = df.to_markdown(index=False)

    # Save to Markdown file
    with open('pipeline_details.md', 'w') as f:
        f.write(md_table)

if __name__ == "__main__":
    generate_json()
    json_to_md()
