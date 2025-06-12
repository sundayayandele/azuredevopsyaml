   
    ‘ABCProductExecutionLimitAPI’
    ‘ABCProductDeterminationAPI’
    ‘ABCPaymentAuxiliaryAPI’
    ‘ABCHello’
I want to use ['run_test_acc_dc1', 'run_test_acc_dc2']  for only the above mentioned applications while for the other I  want to use full_ft_enforce_stage’ in place of ['run_test_acc_dcr', 'run_test_acc_wpr']for the below python script. Kindly assist with a revised python code:

import requests
import json
import warnings
import os
from datetime import datetime, timedelta
warnings.filterwarnings("ignore")

def main():
    start_list = {
    "apps" : [
      {"pipeline": '523, "application" : 'ABCFeedback' },
      {"pipeline": '735’, "application" : 'ABCFeedForward' },
      {"pipeline": '535’, "application" : 'ABCFulfilment' },
      {"pipeline": '547’, "application" : 'ABCInquiry' },
      {"pipeline": '568’, "application" : 'ABCInquiryMessage' },
      {"pipeline": '579, "application" : 'ABCInquiryOrder' },
      {"pipeline": '577’, "application" : 'ABCInquiryTransactionBatch' },
      {"pipeline": '576’, "application" : 'ABCInquiryTransactionRealTime' },
      {"pipeline": '525’, "application" : 'ABCIntake' },
      {"pipeline": '509’, "application" : 'ABCPaymentAuxiliaryAPI' },
      {"pipeline": '529', "application" : 'ABCPaymentInitiationAPI' },
      {"pipeline": '501', "application" : ‘ABCProductDeterminationAPI' },
      {"pipeline": '559', "application" : 'ABCProductExecutionLimitAPI' },
      {"pipeline": '451', "application" : 'ABCPaymentValidationAPI'},
      {"pipeline": '762', "application" : 'ABCRecoveryAPI'},
      {"pipeline": '836', "application" : 'ABCTenantManagement'},
      {"pipeline": '539', "application" : 'ABCValidation'},
      {"pipeline": '764', "application" : 'ABCHello'}
      ]
    }
    list = json.dumps(start_list)
    json_list = json.loads(list)

  for application in json_list['apps']:

        _DEFAULT_TOKEN = os.getenv("SYSTEM_ACCESSTOKEN")
        pipeline_url = "https://dev.azure.com/ABCLTD/ABCOne/_apis/pipelines/" + application['pipeline'] + "/runs?api-version=7.1-preview.1"
    raw_data = requests.get(
        url= pipeline_url,
        verify=False,
        auth=("", _DEFAULT_TOKEN)
    ).json()
    json_dump = json.dumps(raw_data)
    json_object = json.loads(json_dump)
    found='no'
    print(" ")
    print("Looking for a correct run in pipeline :", application['pipeline'] )
    print("This is for application : ", application['application'] )

    for each in json_object['value']:
      try:
        raw_data_2 = requests.get(
        url=f"https://dev.azure.com/ABCLTD/7232-5e9f-3505-078bf7e321a4/_apis/build/builds/{each['id']}/Timeline",
        verify=False,
        auth=("", _DEFAULT_TOKEN)
        ).json()
        json_dump_2 = json.dumps(raw_data_2)
        json_object_2 = json.loads(json_dump_2)
        # Define the time threshold
        thirty_days_ago = datetime.now() - timedelta(days=30)
        for time in json_object_2['records']:
          if time['identifier'] in ['run_test_acc_dc1', 'run_test_acc_dc2'] and time['result'] == 'succeeded' and time['state'] =='completed' :          
            found='yes'
      except:
        print("An exception occurred")

      if found == 'yes' :
        run = each['id']
        app = application['application']
        print(" - Found a succeeded Functional Test in ACC for run ID : ",each['id'] )
        print(f'##vso[task.setvariable variable=buildId_{app};isOutput=true]{run}')
        break
      else:
        print(" - NOT Found a succeeded Functional Test in ACC for run ID : ",each['id'] )

if __name__ == "__main__":
  main()
