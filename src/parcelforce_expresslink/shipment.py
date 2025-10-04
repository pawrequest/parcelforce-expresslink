import datetime as dt
from pathlib import Path
from typing import Self

from pydantic import constr

from parcelforce_expresslink.types import DropOffInd, ShipmentType
from parcelforce_expresslink.address import (
    AddressCollection,
    AddressSender,
    Contact,
    ContactCollection,
    ContactSender,
)
from parcelforce_expresslink.lists import HazardousGoods
from parcelforce_expresslink.models import AddressRecipient, DeliveryOptions
from parcelforce_expresslink.services import ServiceCode
from parcelforce_expresslink.shared import DateTimeRange, Enhancement, PFBaseModel
from parcelforce_expresslink.top import CollectionInfo
# from shipaw.models.ship_types import ShipDirection


class ShipmentReferenceFields(PFBaseModel):
    reference_number1: constr(max_length=24) | None = None
    reference_number2: constr(max_length=24) | None = None
    reference_number3: constr(max_length=24) | None = None
    reference_number4: constr(max_length=24) | None = None
    reference_number5: constr(max_length=24) | None = None
    special_instructions1: constr(max_length=25) | None = None
    special_instructions2: constr(max_length=25) | None = None
    special_instructions3: constr(max_length=25) | None = None
    special_instructions4: constr(max_length=25) | None = None


class Shipment(ShipmentReferenceFields):
    """Needs contract number and department id from settings"""

    shipment_type: ShipmentType = ShipmentType.DELIVERY
    # from settings
    department_id: int = 1
    contract_number: str

    recipient_contact: Contact
    recipient_address: AddressRecipient | AddressCollection
    total_number_of_parcels: int = 1
    shipping_date: dt.date
    service_code: ServiceCode = ServiceCode.EXPRESS24

    # collection
    print_own_label: bool | None = None
    collection_info: CollectionInfo | None = None
    # dropoff
    sender_contact: ContactSender | None = None
    sender_address: AddressSender | None = None

    _label_file: Path | None = (
        None  # must be private for xml serialization to exclude / expresslink to work
    )

    # currently unused (but required by expresslink)
    enhancement: Enhancement | None = None
    delivery_options: DeliveryOptions | None = None
    hazardous_goods: HazardousGoods | None = None
    consignment_handling: bool | None = None
    drop_off_ind: DropOffInd | None = None

    def to_dropoff(self, *, recipient_address, recipient_contact) -> Self:
        if (
            self.collection_info
            or self.shipment_type == ShipmentType.COLLECTION
            or self.sender_contact
            or self.sender_address
        ):
            raise ValueError('Can only convert outbound delivery shipments')
        res = self.model_copy(deep=True)
        res.recipient_address = recipient_address
        res.recipient_contact = recipient_contact
        res.sender_contact = ContactSender.from_recipient(self.recipient_contact)
        res.sender_address = AddressSender.from_recipient(self.recipient_address)
        return res

    def to_inbound(self, *, recipient_address, recipient_contact, own_label=True) -> Self:
        if self.collection_info or self.shipment_type == ShipmentType.COLLECTION:
            raise ValueError('Can only convert outbound delivery shipments')
        res = self.model_copy(deep=True)
        res.shipment_type = ShipmentType.COLLECTION
        res.print_own_label = own_label
        res.collection_info = collection_info_from_recipient(self)
        res.recipient_contact = recipient_contact
        res.recipient_address = recipient_address
        return res

    def __str__(self):
        return f'{self.shipment_type} {f'from {self.collection_info.collection_address.address_line1} ' if self.collection_info else ''}to {self.recipient_address.address_line1}'


def collection_info_from_recipient(shipment):
    return CollectionInfo(
        collection_address=AddressCollection(**shipment.recipient_address.model_dump()),
        collection_contact=(
            ContactCollection.model_validate(
                shipment.recipient_contact.model_dump(exclude={'notifications'})
            )
        ),
        collection_time=DateTimeRange.null_times_from_date(shipment.shipping_date),
    )

