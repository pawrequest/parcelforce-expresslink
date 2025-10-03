from datetime import date

from parcelforce_expresslink.client import ParcelforceClient
from parcelforce_expresslink.address import Contact, AddressRecipient
from parcelforce_expresslink.request_response import ShipmentResponse
from parcelforce_expresslink.shipment import Shipment


def test_readme():
    recip_address = AddressRecipient(
        address_line1="An AddressLine",
        town="A Town",
        postcode="AA1BB2",
    )
    recip_contact = Contact(
        contact_name="A Name",
        email_address="anaddress@adomain.com",
        mobile_phone="07123456789",
        business_name="A Business Name",
    )
    shipment = Shipment(
        recipient_address=recip_address,
        recipient_contact=recip_contact,
        total_number_of_parcels=1,
        shipping_date=date.today(),
    )
    client = ParcelforceClient()
    response: ShipmentResponse = client.request_shipment(shipment)
    assert response.shipment_num is not None




