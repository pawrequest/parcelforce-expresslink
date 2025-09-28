from __future__ import annotations

from enum import StrEnum, Enum


class ShipmentType(StrEnum):
    DELIVERY = 'DELIVERY'
    COLLECTION = 'COLLECTION'


class DropOffInd(StrEnum):
    PO = 'PO'
    DEPOT = 'DEPOT'


class DeliveryKindEnum(str, Enum):
    DELIVERY = 'DELIVERY'
    COLLECTION = 'COLLECTION'


class ExpressLinkError(Exception): ...


class ExpressLinkWarning(Exception): ...


class ExpressLinkNotification(Exception): ...
