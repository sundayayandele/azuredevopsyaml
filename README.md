# azuredevopsyaml
https://www.linkedin.com/in/tititlayo-ayandele-61262b225?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app

https://www.axelos.com/certifications/propath/prince2-project-management/prince2-7-practitioner



- script: |
    echo "##vso[task.setvariable variable=PAT_TOKEN]$(System.AccessToken)"
  displayName: "Set PAT Token"




pathToken = System.getenv("PAT_TOKEN"); // Fetch from environment variable
if (pathToken == null || pathToken.isEmpty()) {
    pathToken = System.getProperty("pat.token", "");
}
LOG.info("VALUE: {}", pathToken);