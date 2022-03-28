from zeep import Client, exceptions
from fastapi import FastAPI, Query

app = FastAPI()

# setup zeep client
client = Client(wsdl="http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl")


@app.get("/check-vat-id")
def check_vat_id(
    state: str = Query(...,
                    description="The country code of the member State. The first two characters of the VAT-ID.",
                    min_length=2,
                    max_length=2,
                    regex="[A-Z]{2}"
                    ),
    vat_number: str = Query(...,
                        description="The actual VAT number (all characters after the country code.",
                        min_length=2,
                        max_length=12,
                        regex="[0-9A-Za-z\+\*\.]{2,12}"
                        )       
):
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

