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