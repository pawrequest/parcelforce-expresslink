import sys
from datetime import date

import parcelforce_expresslink.config
import pytest
from parcelforce_expresslink.client import ParcelforceClient
from parcelforce_expresslink.address import Contact, AddressRecipient
from parcelforce_expresslink.request_response import ShipmentResponse
from parcelforce_expresslink.shipment import Shipment


@pytest.fixture(autouse=True)
def sandbox_only():
    settings = parcelforce_expresslink.config.pf_settings()
    if "test" not in settings.pf_endpoint:
        pytest.skip("Skipping ParcelForce tests outside sandbox environment")
        sys.exit()


def test_readme():
    recip_address = AddressRecipient(
        address_line1="Broadcasting House",
        town="London",
        postcode="W1A 1AA",
    )
    recip_contact = Contact(
        contact_name="A Name",
        email_address="anaddress@adomain.com",
        mobile_phone="07123456789",
        business_name="The BBC",
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




