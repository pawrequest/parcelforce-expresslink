# from __future__ import annotations
#
# from dataclasses import dataclass
# from typing import Self
#
# from shipaw.models.address import Address as AddressAgnost, Contact as ContactAgnost, LongContact
# from shipaw.models.meta import ShippingProvider, register_provider
# from shipaw.models.requests import ProviderName
# from shipaw.models.responses import ShipmentBookingResponseAgnost
# from shipaw.models.services import ServiceDict
# from shipaw.models.shipment import Shipment as ShipmentAgnost
#
# from parcelforce.address import AddressBase, Contact as ContactPF
# from parcelforce_expresslink.client import ParcelforceClient
# from parcelforce_expresslink.combadge import CreateShipmentService
# from parcelforce_expresslink.request_response import ShipmentRequest, ShipmentResponse
# from parcelforce_expresslink.services import ParcelforceServiceDict
# from parcelforce_expresslink.shipment import (
#     Shipment as ShipmentPF,
# )
#
#
# class ParcelforceContact(ContactPF):
#     @classmethod
#     def from_long_contact(cls, long_contact: LongContact) -> Self:
#         return cls(
#             business_name=long_contact.business_name,
#             contact_name=long_contact.contact_name,
#             email_address=long_contact.email_address,
#             mobile_phone=long_contact.mobile_phone,
#         )
#
#
# class ParcelforceAddress(AddressBase):
#     @classmethod
#     def from_long_contact(cls, long_contact: LongContact) -> Self:
#         return cls(
#             address_line1=long_contact.address_lines[0],
#             address_line2=long_contact.address_lines[1] if len(long_contact.address_lines) > 1 else None,
#             address_line3=long_contact.address_lines[2] if len(long_contact.address_lines) > 2 else None,
#             town=long_contact.town,
#             postcode=long_contact.postcode,
#             country=long_contact.country,
#         )
#
#
# @register_provider
# @dataclass
# class ParcelforceShippingProvider(ShippingProvider[ShipmentPF]):
#     name: ProviderName = 'PARCELFORCE'
#     service_dict: ServiceDict = ParcelforceServiceDict
#     shipment_type: type[ShipmentPF] = ShipmentPF
#
#     def book_shipment(self, shipment: dict | ShipmentAgnost) -> ShipmentBookingResponseAgnost:
#         shipment = ShipmentAgnost.model_validate(shipment)
#         shipment_pf = ShipmentPF.from_generic(shipment)
#         shipment_request_pf = ShipmentRequest(requested_shipment=shipment_pf)
#         el_client = ParcelforceClient()
#         authorized_shipment = shipment_request_pf.authenticated(el_client.settings.auth())
#         back = el_client.backend(CreateShipmentService)
#         resp: ShipmentResponse = back.createshipment(request=authorized_shipment.model_dump(by_alias=True))
#         resp.handle_errors()
#
#         resp_agnost = ShipmentBookingResponseAgnost(
#             shipment=shipment,
#             shipment_num=resp.shipment_num,
#             tracking_link=resp.tracking_link(),
#             data=resp.model_dump(),
#             status=resp.status,
#             success=resp.success,
#             label_data=el_client.get_label_content(resp.shipment_num),
#         )
#
#         return resp_agnost
#
#     def get_label_content(self, shipment_num: str) -> bytes:
#         el_client = ParcelforceClient()
#         return el_client.get_label_content(shipment_num)
#
#
# pr: ShippingProvider[ShipmentPF] = ParcelforceShippingProvider()
