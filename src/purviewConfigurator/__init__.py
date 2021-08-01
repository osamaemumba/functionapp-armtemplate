import logging

import azure.functions as func
from requests import *

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    tenant_id = "b790f6ff-34c5-4074-bc2e-2f6be41e5870"
    client_id = "8c6b5be6-2b3c-42d8-9295-e85abf1d2809"
    client_secret = ".pBPb4e753ZEl.a3JBZR_ItpC-e~3_63J3"
    resource_url = "https://purview-api-demo.catalog.purview.azure.com"
    
    output = azuread_auth(tenant_id, client_id, client_secret, resource_url)
    print(output)

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

def azuread_auth(tenant_id: str, client_id: str, client_secret: str, resource_url: str):
    """
    Authenticates Service Principal to the provided Resource URL, and returns the OAuth Access Token
    """
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
    payload= f'grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}&resource={resource_url}'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = request("POST", url, headers=headers, data=payload)
    access_token = json.loads(response.text)['access_token']
    return access_token