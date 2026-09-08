"""Load one bundled seed and compute pure, deterministic previews."""

import json
from importlib.resources import files

from .model import Item, StockroomError, Summary, require_integer


def validated_items(items) -> tuple[Item, ...]:
    # Read at most 17 elements, including the over-limit sentinel.
    result = []
    for item in items:
        if len(result) == 16 or type(item) is not Item:
            raise StockroomError("invalid_catalog")
        result.append(item)
    if not result or len({item.sku for item in result}) != len(result):
        raise StockroomError("invalid_catalog")
    return tuple(sorted(result, key=lambda item: item.sku))


def _unique_fields(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise StockroomError("invalid_catalog")
        result[key] = value
    return result


def decode_catalog(data: bytes) -> tuple[Item, ...]:
    if len(data) > 4096:
        raise StockroomError("invalid_catalog")
    try:
        records = json.loads(data.decode("utf-8"), object_pairs_hook=_unique_fields)
        if type(records) is not list or not 1 <= len(records) <= 16:
            raise StockroomError("invalid_catalog")
        expected = {"sku", "on_hand", "reserved", "reorder_level"}
        if any(type(record) is not dict or set(record) != expected for record in records):
            raise StockroomError("invalid_catalog")
        return validated_items(Item(**record) for record in records)
    except (UnicodeError, ValueError, TypeError, RecursionError):
        raise StockroomError("invalid_catalog") from None


def load_catalog() -> tuple[Item, ...]:
    try:
        resource = files("stockroom").joinpath("data", "catalog.json")
        with resource.open("rb") as stream:
            return decode_catalog(stream.read(4097))
    except (OSError, ValueError):
        raise StockroomError("invalid_catalog") from None


def summarize(items) -> Summary:
    return Summary(validated_items(items))


def reorder_items(items) -> tuple[Item, ...]:
    return tuple(item for item in validated_items(items) if item.needs_reorder)


def reserve_preview(items, sku: str, quantity: int) -> Item:
    require_integer(quantity, 1, 1000, "invalid_quantity")
    catalog = validated_items(items)
    item = next((item for item in catalog if item.sku == sku), None)
    if item is None:
        raise StockroomError("unknown_sku")
    if quantity > item.available:
        raise StockroomError("insufficient_stock")
    return Item(item.sku, item.on_hand, item.reserved + quantity, item.reorder_level)
