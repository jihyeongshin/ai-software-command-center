import builtins
import io
import unittest
from pathlib import Path
from unittest.mock import patch

from stockroom.cli import main
from stockroom.model import StockroomError


SUMMARY = (
    b'{"items":[{"available":10,"needs_reorder":false,"on_hand":12,"reorder_level":3,"reserved":2,"sku":"BOX-A"},'
    b'{"available":0,"needs_reorder":true,"on_hand":5,"reorder_level":2,"reserved":5,"sku":"BOX-B"},'
    b'{"available":3,"needs_reorder":true,"on_hand":4,"reorder_level":3,"reserved":1,"sku":"BOX-C"}],"total_available":13}\n'
)
RESERVE = b'{"available":6,"needs_reorder":false,"on_hand":12,"reorder_level":3,"reserved":6,"sku":"BOX-A"}\n'


def invoke(*args):
    out, err = io.BytesIO(), io.BytesIO()
    code = main(args, stdout=out, stderr=err)
    return code, out.getvalue(), err.getvalue()


class CliTests(unittest.TestCase):
    def test_summary_exact_json(self):
        self.assertEqual(invoke("summary"), (0, SUMMARY, b""))
        self.assertLessEqual(len(SUMMARY), 4096)
        self.assertEqual(SUMMARY.count(b"\n"), 1)

    def test_reserve_exact_json(self):
        self.assertEqual(invoke("reserve", "--sku", "BOX-A", "--quantity", "4"), (0, RESERVE, b""))
        self.assertEqual(invoke("reserve", "--quantity", "4", "--sku", "BOX-A"), (0, RESERVE, b""))

    def test_business_error_json_and_exit(self):
        cases = [("BOX-A", "11", "insufficient_stock"), ("MISSING", "1", "unknown_sku")]
        cases += [("BOX-A", q, "invalid_quantity") for q in
                  ("0", "1001", "-1", "1.0", "True", "", "1" * 5000, "\u0661", "+1")]
        for sku, quantity, error in cases:
            with self.subTest(error=error, quantity=quantity[:12]):
                result = invoke("reserve", "--sku", sku, "--quantity", quantity)
                expected = ('{"error":"' + error + '"}\n').encode("ascii")
                self.assertEqual(result, (2, b"", expected))
        with patch("stockroom.cli.load_catalog", side_effect=StockroomError("invalid_catalog")):
            self.assertEqual(invoke("summary"), (2, b"", b'{"error":"invalid_catalog"}\n'))

    def test_unknown_command_or_option_rejected(self):
        cases = [(), ("unknown",), ("--help",), ("summary", "--input", "catalog.json"),
                 ("reserve",), ("reserve", "--sku", "BOX-A", "--sku", "BOX-B"),
                 ("reserve", "--sku", "BOX-A", "--url", "https://invalid.example"),
                 ("reserve", "--sku", "BOX-A", "--quantity", "4", "--config", "x")]
        for args in cases:
            with self.subTest(args=args):
                self.assertEqual(invoke(*args), (2, b"", b'{"error":"invalid_arguments"}\n'))

    def test_repeated_invocation_identical(self):
        seed = Path(__file__).resolve().parents[1] / "stockroom/data/catalog.json"
        before = seed.read_bytes()
        for _ in range(3):
            self.assertEqual(invoke("summary"), (0, SUMMARY, b""))
            self.assertEqual(invoke("reserve", "--sku", "BOX-A", "--quantity", "4"), (0, RESERVE, b""))
        self.assertEqual(seed.read_bytes(), before)

    def test_cli_has_no_write_or_network_path(self):
        # Bounded example behavior only; these guards are not sandbox proof.
        original_open, original_io_open = builtins.open, io.open

        def read_only(original):
            def guarded(file, mode="r", *args, **kwargs):
                self.assertFalse(any(flag in mode for flag in "wax+"))
                return original(file, mode, *args, **kwargs)
            return guarded

        with patch("builtins.open", side_effect=read_only(original_open)), \
             patch("io.open", side_effect=read_only(original_io_open)), \
             patch("os.open", side_effect=AssertionError("unexpected low-level open")), \
             patch("socket.socket", side_effect=AssertionError("unexpected network")), \
             patch("socket.create_connection", side_effect=AssertionError("unexpected network")):
            self.assertEqual(invoke("summary"), (0, SUMMARY, b""))
            self.assertEqual(invoke("reserve", "--sku", "BOX-A", "--quantity", "4"), (0, RESERVE, b""))
            self.assertEqual(invoke("summary", "--output", "x")[0], 2)
