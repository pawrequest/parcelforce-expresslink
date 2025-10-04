from parcelforce_expresslink.address import AddressRecipient, Contact
from parcelforce_expresslink.request_response import ShipmentResponse
from parcelforce_expresslink.shared import DateTimeRange
from parcelforce_expresslink.types import ShipmentType


def test_client_gets_candidates(sample_client, sample_address):
    addresses = sample_client.get_candidates(sample_address.postcode)
    assert isinstance(addresses, list)
    assert isinstance(addresses[0], AddressRecipient)
    assert addresses[0].postcode == sample_address.postcode


def check_label(sample_client, resp, tmp_path):
    label_data = sample_client.get_label_content(ship_num=resp.shipment_num)
    output = tmp_path / f'{resp.shipment_num}.pdf'
    output.write_bytes(label_data)
    assert output.exists()


def test_client_sends_outbound(sample_shipment, sample_client, tmp_path):
    resp = sample_client.request_shipment(sample_shipment)
    assert isinstance(resp, ShipmentResponse)
    assert not resp.alerts
    check_label(sample_client, resp, tmp_path)


def test_to_inbound(sample_inbound_shipment, sample_shipment):
    ...
    og_recipient_contact = sample_shipment.recipient_contact.model_dump(exclude={'notifications'})

    c = sample_inbound_shipment.collection_info
    collection_contact = c.collection_contact.model_dump(exclude={'notifications'})

    converted_back_recip = Contact.model_validate(
        collection_contact, from_attributes=True
    ).model_dump(exclude={'notifications'})
    assert og_recipient_contact == converted_back_recip
    assert sample_inbound_shipment.shipment_type == ShipmentType.COLLECTION
    assert sample_inbound_shipment.print_own_label == True
    assert c.collection_address.model_dump() == sample_shipment.recipient_address.model_dump()
    assert c.collection_time == DateTimeRange.null_times_from_date(sample_shipment.shipping_date)


def test_to_dropoff(sample_dropoff_shipment, sample_shipment):
    ...
    og_recipient_contact = sample_shipment.recipient_contact.model_dump(exclude={'notifications'})
    og_recipient_address = sample_shipment.recipient_address.model_dump()

    sender_contact = sample_dropoff_shipment.sender_contact.model_dump(exclude={'notifications'})
    sender_address = sample_dropoff_shipment.sender_address.model_dump()

    converted_back_recip = Contact.model_validate(sender_contact, from_attributes=True).model_dump(
        exclude={'notifications'}
    )
    assert og_recipient_contact == converted_back_recip
    assert og_recipient_address == sender_address
    assert sample_dropoff_shipment.shipment_type == ShipmentType.DELIVERY
    assert sample_dropoff_shipment.print_own_label is None
    assert sample_dropoff_shipment.collection_info is None


def test_client_sends_inbound(sample_inbound_shipment, sample_client, tmp_path):
    resp = sample_client.request_shipment(sample_inbound_shipment)
    assert isinstance(resp, ShipmentResponse)
    assert not resp.alerts
    check_label(sample_client, resp, tmp_path)


def test_client_sends_dropoff(sample_dropoff_shipment, sample_client, tmp_path):
    resp = sample_client.request_shipment(sample_dropoff_shipment)
    assert isinstance(resp, ShipmentResponse)
    assert not resp.alerts
    check_label(sample_client, resp, tmp_path)



