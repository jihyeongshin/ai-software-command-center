"""Two fixed commands; compact ASCII JSON on exactly one output stream."""

import json
import sys

from .inventory import load_catalog, reserve_preview, summarize
from .model import StockroomError


def _parse(argv: list[str]) -> tuple[str, str | None, int | None]:
    if argv == ["summary"]:
        return "summary", None, None
    if len(argv) != 5 or argv[0] != "reserve":
        raise StockroomError("invalid_arguments")
    if set(argv[1::2]) != {"--sku", "--quantity"}:
        raise StockroomError("invalid_arguments")
    options = dict(zip(argv[1::2], argv[2::2]))
    text = options["--quantity"]
    # Bound decimal parsing before conversion; Unicode digits are not accepted.
    if not 1 <= len(text) <= 4 or any(char not in "0123456789" for char in text):
        raise StockroomError("invalid_quantity")
    return "reserve", options["--sku"], int(text)


def _encode(value: dict) -> bytes:
    encoded = (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("ascii")
    if len(encoded) > 4096:
        raise StockroomError("output_limit")
    return encoded


def main(argv=None, *, stdout=None, stderr=None) -> int:
    out = sys.stdout.buffer if stdout is None else stdout
    err = sys.stderr.buffer if stderr is None else stderr
    try:
        command, sku, quantity = _parse(list(sys.argv[1:] if argv is None else argv))
        items = load_catalog()
        result = summarize(items) if command == "summary" else reserve_preview(items, sku, quantity)
        payload = _encode(result.as_dict())
    except StockroomError as error:
        err.write(_encode({"error": str(error)}))
        return 2
    out.write(payload)
    return 0
