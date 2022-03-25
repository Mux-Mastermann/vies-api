from zeep import Client, exceptions
from fastapi import FastAPI, Query

app = FastAPI()

# setup zeep client
client = Client(wsdl="http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl")


@app.get("/check-vat-id")
def check_vat_id(*, state: str = Query(default=None, description="The abbreviaiton of the member state."), vat_number: str):
    """
    Checks via the official SOAP service of the EU if a VAT ID is valid.
    
    If an error occurs, returns the error message, else returns the full response object.

    """
    success = None
    try:
        response = client.service.checkVat(state, vat_number)
    except exceptions.Fault as e:
        error_message = e.message
        success = False
        return {"success": success, "error_message": error_message}
    else:
        success = True
        return {"success": success, "data": response}

