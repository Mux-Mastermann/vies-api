import datetime

from zeep import Client, exceptions, helpers
from fastapi import FastAPI, Query, Depends     # Depends is necessary to use Vat_id class as model for Query Parameters (see check_vat_id function parameters). Otherwise it would be used as model for body.
from fastapi.responses import RedirectResponse
from typing import Optional
from pydantic import BaseModel


__version__ = "0.2.0"
SOAP_URL = "http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl"


# INPUT Model of the query parameters
class Vat_id(BaseModel):
    state: str = Query(...,
                    description="The country code of the member State. The first two characters of the VAT-ID.",
                    min_length=2,
                    max_length=2,
                    regex="[A-Z]{2}"
                    )
    vat_number: str = Query(...,
                        description="The actual VAT number (all characters after the country code.",
                        min_length=2,
                        max_length=12,
                        regex="[0-9A-Za-z\+\*\.]{2,12}"
                        )


# OUTPUT model that is received via VIES when the request is successful
class Vies_data(BaseModel):
    countryCode: str
    vatNumber: str
    requestDate: datetime.date
    valid: bool
    name: str
    address: str

# OUTPUT response model which is returned from the vies-api
class Response(BaseModel):
    success: str
    data: Optional[Vies_data]
    error_message: Optional[str]


# initialize Fastapi with some meta data
app = FastAPI(title="VIES-API", description="For easy interaction with the VIES VAT-ID Validation service of the European Commission.", version=__version__)

# setup zeep client for interacting with the SOAP service
client = Client(wsdl=SOAP_URL)


@app.get("/check-vat-id", response_model=Response, tags=["VAT Validation"], summary="Validate VAT-ID")
def check_vat_id(vat_id: Vat_id=Depends()):
    """Validates a given VAT-ID. If available also returns the name and address of the company."""
    success = None
    try:
        response = client.service.checkVat(vat_id.state, vat_id.vat_number)
    except exceptions.Fault as e:
        error_message = e.message
        success = False
        return {"success": success, "error_message": error_message}
    else:
        data = helpers.serialize_object(response)
        success = True
        return {"success": success, "data": data}
