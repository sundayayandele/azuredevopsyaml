trigger: none  # The orchestrator does not trigger automatically

resources:
  pipelines:
    - pipeline: Power1Pipeline
      source: Power1
      trigger: none  # Ensure this pipeline doesn't trigger automatically

    - pipeline: Power2Pipeline
      source: Power2
      trigger: none  # Ensure this pipeline doesn't trigger automatically

parameters:
  environment: 'production'
  deploymentRegion: 'us-east'

stages:
  - stage: TriggerPower1
    displayName: "Trigger Power1 Pipeline"
    jobs:
      - job: TriggerPower1Job
        steps:
          - script: echo "Triggering Power1 Pipeline"
          - script: |
              echo "##vso[build.queue name=Power1;parameters.environment=${{ parameters.environment }};parameters.deploymentRegion=${{ parameters.deploymentRegion }}]"
  
  - stage: TriggerPower2
    displayName: "Trigger Power2 Pipeline"
    dependsOn: TriggerPower1
    jobs:
      - job: TriggerPower2Job
        steps:
          - script: echo "Triggering Power2 Pipeline"
          - script: |
              echo "##vso[build.queue name=Power2;parameters.environment=${{ parameters.environment }};parameters.deploymentRegion=${{ parameters.deploymentRegion }}]"




---------------------------


# orchestrator.yaml - Pipeline to run power1.yaml and power2.yaml using REST API

trigger: none # Manual trigger only

parameters:
  - name: pipelineToRun
    displayName: 'Pipeline to Run'
    type: string
    default: 'both'
    values:
      - 'power1'
      - 'power2'
      - 'both'
  
  # Parameters for power1 pipeline
  - name: power1Parameters
    displayName: 'Power1 Parameters (JSON format)'
    type: string
    default: '{}'
  
  # Parameters for power2 pipeline
  - name: power2Parameters
    displayName: 'Power2 Parameters (JSON format)'
    type: string
    default: '{}'

variables:
  # Replace these with your organization and project names
  organization: 'YourOrganization'
  project: 'YourProject'
  
  # Replace these with your actual pipeline IDs
  power1PipelineId: '1'  # ID of the pipeline defined by power1.yaml
  power2PipelineId: '2'  # ID of the pipeline defined by power2.yaml

pool:
  vmImage: 'ubuntu-latest'

stages:
  - stage: TriggerPipelines
    jobs:
      - job: RunPower1
        condition: or(eq('${{ parameters.pipelineToRun }}', 'power1'), eq('${{ parameters.pipelineToRun }}', 'both'))
        steps:
          - task: PowerShell@2
            displayName: 'Trigger Power1 Pipeline'
            inputs:
              targetType: 'inline'
              script: |
                # Get user-provided parameters
                $parameters = '${{ parameters.power1Parameters }}'
                
                # Create the request body
                $body = @{
                  parameters = $parameters
                } | ConvertTo-Json
                
                # Use the Azure DevOps REST API to trigger the pipeline
                $url = "https://dev.azure.com/$(organization)/$(project)/_apis/pipelines/$(power1PipelineId)/runs?api-version=6.0"
                
                # Use the system access token
                $token = "$(System.AccessToken)"
                $base64AuthInfo = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(":$token"))
                
                $headers = @{
                  Authorization = "Basic $base64AuthInfo"
                  "Content-Type" = "application/json"
                }
                
                # Trigger the pipeline
                $response = Invoke-RestMethod -Uri $url -Method Post -Headers $headers -Body $body
                
                # Output the run ID for tracking
                Write-Host "Triggered Power1 Pipeline. Run ID: $($response.id)"
            env:
              SYSTEM_ACCESSTOKEN: $(System.AccessToken)
      
      - job: RunPower2
        condition: or(eq('${{ parameters.pipelineToRun }}', 'power2'), eq('${{ parameters.pipelineToRun }}', 'both'))
        dependsOn: RunPower1
        steps:
          - task: PowerShell@2
            displayName: 'Trigger Power2 Pipeline'
            inputs:
              targetType: 'inline'
              script: |
                # Get user-provided parameters
                $parameters = '${{ parameters.power2Parameters }}'
                
                # Create the request body
                $body = @{
                  parameters = $parameters
                } | ConvertTo-Json
                
                # Use the Azure DevOps REST API to trigger the pipeline
                $url = "https://dev.azure.com/$(organization)/$(project)/_apis/pipelines/$(power2PipelineId)/runs?api-version=6.0"
                
                # Use the system access token
                $token = "$(System.AccessToken)"
                $base64AuthInfo = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(":$token"))
                
                $headers = @{
                  Authorization = "Basic $base64AuthInfo"
                  "Content-Type" = "application/json"
                }
                
                # Trigger the pipeline
                $response = Invoke-RestMethod -Uri $url -Method Post -Headers $headers -Body $body
                
                # Output the run ID for tracking
                Write-Host "Triggered Power2 Pipeline. Run ID: $($response.id)"
            env:
              SYSTEM_ACCESSTOKEN: $(System.AccessToken)
__________&_&&&&______________&&&&&___________&&

Got it! You want the orchestrator pipeline to trigger the Power1 and Power2 pipelines while passing parameters.

Alternative Approaches Without AzurePipelinesRunPipeline@1

Instead of using the AzurePipelinesRunPipeline@1 task, you can trigger child pipelines using pipeline resources with trigger: none and the REST API (InvokeRESTAPI task) or resources.pipelines approach.


---

Solution 1: Using resources.pipelines to Trigger Power1 and Power2

This approach ensures that the orchestrator pipeline triggers Power1 and Power2 as separate pipeline runs.

orchestrator.yaml

trigger: none  # The orchestrator does not trigger automatically

resources:
  pipelines:
    - pipeline: Power1Pipeline
      source: Power1
      trigger: none  # Ensure this pipeline doesn't trigger automatically

    - pipeline: Power2Pipeline
      source: Power2
      trigger: none  # Ensure this pipeline doesn't trigger automatically

parameters:
  environment: 'production'
  deploymentRegion: 'us-east'

stages:
  - stage: TriggerPower1
    displayName: "Trigger Power1 Pipeline"
    jobs:
      - job: TriggerPower1Job
        steps:
          - script: echo "Triggering Power1 Pipeline"
          - script: |
              echo "##vso[build.queue name=Power1;parameters.environment=${{ parameters.environment }};parameters.deploymentRegion=${{ parameters.deploymentRegion }}]"
  
  - stage: TriggerPower2
    displayName: "Trigger Power2 Pipeline"
    dependsOn: TriggerPower1
    jobs:
      - job: TriggerPower2Job
        steps:
          - script: echo "Triggering Power2 Pipeline"
          - script: |
              echo "##vso[build.queue name=Power2;parameters.environment=${{ parameters.environment }};parameters.deploymentRegion=${{ parameters.deploymentRegion }}]"


---

Solution 2: Using REST API to Trigger Power1 and Power2

If you want more flexibility and control, you can trigger pipelines using Azure DevOps REST API.

orchestrator.yaml (REST API Method)

trigger: none

parameters:
  environment: 'production'
  deploymentRegion: 'us-east'

variables:
  azureDevOpsOrgUrl: "https://dev.azure.com/YourOrganization"
  projectName: "YourProject"
  personalAccessToken: "$(PAT_TOKEN)"  # Store this in a secure variable group

stages:
  - stage: TriggerPower1
    displayName: "Trigger Power1 Pipeline"
    jobs:
      - job: TriggerPower1Job
        steps:
          - task: PowerShell@2
            displayName: "Trigger Power1 Pipeline via REST API"
            inputs:
              targetType: 'inline'
              script: |
                $uri = "$(azureDevOpsOrgUrl)/$(projectName)/_apis/pipelines/Power1/runs?api-version=6.0-preview.1"
                $body = @{
                  resources = @{ repositories = @{ self = @{ refName = 'refs/heads/main' } } }
                  templateParameters = @{
                    environment = "${{ parameters.environment }}"
                    deploymentRegion = "${{ parameters.deploymentRegion }}"
                  }
                } | ConvertTo-Json -Depth 10
                
                $headers = @{
                  Authorization = "Basic $(echo -n ":$(personalAccessToken)" | base64)"
                  "Content-Type" = "application/json"
                }
                
                Invoke-RestMethod -Uri $uri -Method Post -Headers $headers -Body $body

  - stage: TriggerPower2
    displayName: "Trigger Power2 Pipeline"
    dependsOn: TriggerPower1
    jobs:
      - job: TriggerPower2Job
        steps:
          - task: PowerShell@2
            displayName: "Trigger Power2 Pipeline via REST API"
            inputs:
              targetType: 'inline'
              script: |
                $uri = "$(azureDevOpsOrgUrl)/$(projectName)/_apis/pipelines/Power2/runs?api-version=6.0-preview.1"
                $body = @{
                  resources = @{ repositories = @{ self = @{ refName = 'refs/heads/main' } } }
                  templateParameters = @{
                    environment = "${{ parameters.environment }}"
                    deploymentRegion = "${{ parameters.deploymentRegion }}"
                  }
                } | ConvertTo-Json -Depth 10
                
                $headers = @{
                  Authorization = "Basic $(echo -n ":$(personalAccessToken)" | base64)"
                  "Content-Type" = "application/json"
                }
                
                Invoke-RestMethod -Uri $uri -Method Post -Headers $headers -Body $body


---

Comparison of Solutions


---

Which One Should You Use?

Use resources.pipelines with ##vso[build.queue] if you want a simple way to trigger Power1 and Power2.

Use REST API (Invoke-RestMethod) if:

You need advanced control over pipeline execution.

You want to trigger pipelines dynamically with custom parameters.

You are triggering pipelines outside Azure DevOps (e.g., from external systems).



Would you like help setting up a Personal Access Token (PAT) for the REST API method?

