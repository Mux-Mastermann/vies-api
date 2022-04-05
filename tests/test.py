import requests

def check_vat_id(state: str, vat_number: str):

    endpoint = "https://vies-api.deta.dev/check-vat-id"

    parameter = {
    "state": state,
    "vat_number": vat_number
    }

    response = requests.get(url=endpoint, params=parameter)

    return response.json()

print(check_vat_id("DE", "123456789"))