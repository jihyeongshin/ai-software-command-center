import json
import unittest
from dataclasses import FrozenInstanceError

from stockroom.inventory import decode_catalog, load_catalog, reorder_items, reserve_preview, summarize
from stockroom.model import Item, StockroomError


class InventoryTests(unittest.TestCase):
    def test_seed_summary(self):
        result = summarize(load_catalog())
        self.assertEqual(result.total_available, 13)
        self.assertEqual([(i.sku, i.available) for i in result.items],
                         [("BOX-A", 10), ("BOX-B", 0), ("BOX-C", 3)])

    def test_reorder_threshold_inclusive(self):
        self.assertEqual([i.sku for i in reorder_items(load_catalog())], ["BOX-B", "BOX-C"])
        self.assertTrue(Item("X", 3, 0, 3).needs_reorder)
        self.assertFalse(Item("X", 4, 0, 3).needs_reorder)
        self.assertTrue(Item("X", 0, 0, 0).needs_reorder)

    def test_reservation_preview(self):
        item = reserve_preview(load_catalog(), "BOX-A", 4)
        self.assertEqual((item.on_hand, item.reserved, item.available), (12, 6, 6))
        self.assertFalse(item.needs_reorder)

    def test_reservation_exact_availability(self):
        item = reserve_preview(load_catalog(), "BOX-A", 10)
        self.assertEqual((item.reserved, item.available, item.needs_reorder), (12, 0, True))

    def test_insufficient_stock(self):
        for sku, quantity in (("BOX-A", 11), ("BOX-B", 1), ("BOX-C", 4)):
            with self.subTest(sku=sku), self.assertRaisesRegex(StockroomError, "^insufficient_stock$"):
                reserve_preview(load_catalog(), sku, quantity)

    def test_unknown_sku(self):
        for sku in ("MISSING", "", "box-a", "../catalog.json"):
            with self.subTest(sku=sku), self.assertRaisesRegex(StockroomError, "^unknown_sku$"):
                reserve_preview(load_catalog(), sku, 1)

    def test_quantity_and_record_bounds(self):
        for quantity in (True, False, 0, -1, 1001, 1.0, "1", None):
            with self.subTest(quantity=quantity), self.assertRaisesRegex(StockroomError, "^invalid_quantity$"):
                reserve_preview(load_catalog(), "BOX-A", quantity)
        for field in ("on_hand", "reserved", "reorder_level"):
            for value in (True, False, -1, 1001, 0.5, "0", None):
                record = dict(sku="X", on_hand=1000, reserved=0, reorder_level=0)
                record[field] = value
                with self.subTest(field=field, value=value), self.assertRaises(StockroomError):
                    Item(**record)
        self.assertEqual(reserve_preview([Item("X", 1000, 0, 1000)], "X", 1000).available, 0)
        self.assertEqual(summarize([Item("X", 0, 0, 0)]).total_available, 0)
        with self.assertRaises(StockroomError):
            Item("X", 0, 1, 0)
        for items in ([], [Item("X", 1, 0, 0)] * 2,
                      [Item(str(i), 1, 0, 0) for i in range(17)]):
            with self.subTest(count=len(items)), self.assertRaises(StockroomError):
                summarize(items)
        self.assertEqual(len(summarize([Item(str(i), 1, 0, 0) for i in range(16)]).items), 16)
        record = [{"sku": "X", "on_hand": 1, "reserved": 0, "reorder_level": 0}]
        seed = json.dumps(record).encode()
        self.assertEqual(len(decode_catalog(seed + b" " * (4096 - len(seed)))), 1)
        with self.assertRaises(StockroomError):
            decode_catalog(seed + b" " * (4097 - len(seed)))

    def test_input_immutability_and_sorting(self):
        items = list(reversed(load_catalog()))
        before = tuple(items)
        summary = summarize(items)
        preview = reserve_preview(items, "BOX-A", 4)
        reorder_items(items)
        self.assertEqual(tuple(items), before)
        self.assertEqual([i.sku for i in summary.items], ["BOX-A", "BOX-B", "BOX-C"])
        self.assertEqual(load_catalog()[0].reserved, 2)
        self.assertIsNot(preview, summary.items[0])
        with self.assertRaises(FrozenInstanceError):
            preview.reserved = 9
        with self.assertRaises(FrozenInstanceError):
            summary.items = ()
