import requests
import msal
import os
# creds file just contains the following:
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

def request_access_token():
    app_id = '0ee35dbb-058a-4f5a-b02e-d55f13f9c8d7'
    tenant_id = '045d9a38-9d51-499c-9b4e-f1caeefcf04c'

    authority_url = 'https://login.microsoftonline.com/' + tenant_id
    scopes = ['https://analysis.windows.net/powerbi/api/.default']

    # Step 1. Generate Power BI Access Token
    client = msal.PublicClientApplication(app_id, authority=authority_url)
    token_response = client.acquire_token_by_username_password(
        username=username, password=password, scopes=scopes)
    if not 'access_token' in token_response:
        raise Exception(token_response['error_description'])

    access_id = token_response.get('access_token')
    return access_id

def response1():
    access_id = request_access_token()
    dataset_id = 'a8d8303f-d266-48ee-87a8-d5d29cdede59'
    #dataset_id = '49d44d6b-9680-4764-ae81-f87ab01deee5'
    endpoint = f'https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/refreshes'
    headers = {
    'Authorization': f'Bearer ' + access_id
    }

    response1 = requests.post(endpoint, headers=headers)
    if response1.status_code == 202:
        print(f'Dataset {dataset_id} refreshed')
    else:
        print(f'Dataset {dataset_id} NOT refreshed')
        print(response1.reason)
        print(response1.json())

if __name__ == "__main__":
    response1()
