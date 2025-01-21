#!/bin/bash
set -e

# Validate environment argument
if [[ -z "$1" ]]; then
    echo "Error: Environment not specified. Please provide the environment (DT, Acc, PTF) as an argument."
    exit 1
fi

environment="$1"  # Environment argument (DT, Acc, PTF)

# Define variables (or pass them as parameters to this script)
directory="/path/to/directory"
user="your_user"
pass="your_password"
configurations="your_configurations"

# List of all watchers (including snapshotfailedalert.json)
ALL_WATCHERS=(
    "snapshotfailedalert.json"
    "watcher2.json"
    "watcher3.json"
    ...
    "watcher25.json"
)

# Define watchers excluded from PTF
PTF_EXCLUDED_WATCHERS=("watcher24.json" "watcher25.json")  # List of 2 watchers not allowed in PTF

# Loop through all watchers and deploy them based on the environment
for watcher in "${ALL_WATCHERS[@]}"; do
    echo "Processing watcher: $watcher"

    # Check if the watcher should be deployed in the current environment
    if [[ "$environment" == "PTF" ]]; then
        if [[ " ${PTF_EXCLUDED_WATCHERS[*]} " =~ " ${watcher} " ]]; then
            echo "Watcher '$watcher' is not allowed in PTF environment. Skipping..."
            continue
        fi
    fi

    # Call runcommand_alerts.sh for the watcher
    bash pipelines/_scripts/runcommand_alerts.sh \
      -f "$watcher" \
      -d "$directory" \
      -u "$user" \
      -p "$pass" \
      -c "$configurations" \
      -e "$environment"
done
========[===================≠=
runcmd
===≠======

#!/bin/bash
set -e

# Define flags
while getopts d:f:u:p:c:e: flag
do
    case "${flag}" in
        f) filename=${OPTARG};;
        d) directory=${OPTARG};;
        u) user=${OPTARG};;
        p) pass=${OPTARG};;
        c) configurations=${OPTARG};;
        e) environment=${OPTARG};;  # Environment flag
    esac
done

# Validate environment
if [[ -z "$environment" ]]; then
    echo "Error: Environment not specified. Use -e to specify the environment (DT, Acc, PTF)."
    exit 1
fi

# Add your logic to deploy the watcher here
# Example: curl or API call to deploy watcher
echo "Deploying watcher '$filename' in $environment environment..."
echo "Using directory: $directory, user: $user, configurations: $configurations"

========≠=========
azure pipeline.yaml
=========

parameters:
  - name: environment
    displayName: 'Environment'
    type: string
    default: 'DT'
    values:
      - 'DT'
      - 'Acc'
      - 'PTF'

jobs:
  - job: DeployWatchers
    displayName: 'Deploy Watchers'
    steps:
      - script: |
          bash pipelines/_scripts/setupelkaas.sh "${{ parameters.environment }}"
        displayName: 'Run Setup ELKaaS Script'
        env:
          directory: $(directory)
          user: $(user)
          pass: $(pass)
          configurations: $(configurations)

