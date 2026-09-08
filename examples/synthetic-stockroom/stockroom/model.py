"""Immutable integer domain values; no persistence or runtime integration."""

from dataclasses import dataclass


class StockroomError(ValueError):
    """A stable public error code, never an input value or host exception."""


def require_integer(value: int, minimum: int, maximum: int, code: str) -> None:
    if type(value) is not int or not minimum <= value <= maximum:
        raise StockroomError(code)


@dataclass(frozen=True, slots=True)
class Item:
    sku: str
    on_hand: int
    reserved: int
    reorder_level: int

    def __post_init__(self) -> None:
        if type(self.sku) is not str or not self.sku:
            raise StockroomError("invalid_catalog")
        for value in (self.on_hand, self.reserved, self.reorder_level):
            require_integer(value, 0, 1000, "invalid_catalog")
        if self.reserved > self.on_hand:
            raise StockroomError("invalid_catalog")

    @property
    def available(self) -> int:
        return self.on_hand - self.reserved

    @property
    def needs_reorder(self) -> bool:
        return self.available <= self.reorder_level

    def as_dict(self) -> dict:
        return {
            "sku": self.sku,
            "on_hand": self.on_hand,
            "reserved": self.reserved,
            "reorder_level": self.reorder_level,
            "available": self.available,
            "needs_reorder": self.needs_reorder,
        }


@dataclass(frozen=True, slots=True)
class Summary:
    items: tuple[Item, ...]

    @property
    def total_available(self) -> int:
        return sum(item.available for item in self.items)

    def as_dict(self) -> dict:
        return {
            "items": [item.as_dict() for item in self.items],
            "total_available": self.total_available,
        }
