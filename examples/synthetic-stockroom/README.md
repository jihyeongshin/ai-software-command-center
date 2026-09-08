# Synthetic Stockroom

Project-authored synthetic public example candidate for AISCC P2-2. Three artificial
stock records demonstrate availability, inclusive reorder thresholds, and reservation
previews. No external data, network, provider, database, server, private data, or
third-party runtime dependency is used. CPython **3.12.14 exactly** is required;
provisioning the interpreter is outside this example.

Run these commands from `examples/synthetic-stockroom/` with that interpreter:

```text
python -I -B -c "import sys; assert sys.version_info[:3] == (3, 12, 14)"
python -E -s -B -m unittest discover -s tests -p "test_*.py" -v
python -I -B tools/build.py
python -I -B .build/stockroom.pyz summary
python -I -B .build/stockroom.pyz reserve --sku BOX-A --quantity 4
python -E -s -B -m stockroom summary
python -E -s -B -m stockroom reserve --sku BOX-A --quantity 4
```

Use `-B` to avoid bytecode residue. Tests and the builder write only
`.build/stockroom.pyz`; remove this exact generated file after capturing evidence.
No install step is needed. Rebuilding unchanged inputs yields identical bytes.
The archive uses stored entries with fixed order, timestamps and permissions.
It contains a constant launcher and the six package/data files, with no tests or docs.
This development build artifact is not sandbox or runtime-isolation proof.

## Domain and input contract

The bundled catalog has BOX-A `(12, 2, 3)`, BOX-B `(5, 5, 2)`, and BOX-C `(4, 1, 3)`
as `(on_hand, reserved, reorder_level)`. Availability is `on_hand - reserved`;
reorder is required when availability is **less than or equal to** the threshold.
Total availability is 13. Catalogs contain 1..16 records with unique, nonempty
string SKUs and exactly the four seed fields. Encoded seed size is at most 4096
bytes. Each count is an integer excluding bool, in 0..1000; reserved cannot exceed
on-hand stock. Reservation quantity is an integer excluding bool, in 1..1000,
and cannot exceed available stock.

The CLI accepts only `summary` or `reserve --sku <SKU> --quantity <INTEGER>`.
The two reserve options may be reordered; duplicates and other options are rejected.
Quantity text uses 1..4 ASCII decimal digits, with a resulting value in 1..1000.
There is no path, URL, upload, config, plugin, free-form task or shell input.

Success exits 0 with one compact ASCII JSON object plus LF on stdout and empty
stderr. Keys are sorted; summary items are sorted by SKU; output is at most 4096
bytes. Reserve returns the preview item, with BOX-A quantity 4 yielding on_hand 12,
reserved 6 and available 6. Every invocation loads the same seed; no seed or
durable state is written. Module and archive commands produce identical bytes.

Argument/business errors exit 2, leave stdout empty, and emit one compact JSON
object plus LF on stderr. Stable codes are `invalid_arguments`, `invalid_quantity`,
`unknown_sku`, `insufficient_stock`, `invalid_catalog`, and `output_limit`.
Errors do not echo input, tracebacks or host paths.

## Future work boundary

Controlled future change surfaces are the availability/reorder/reservation rules,
CLI serialization/validation, seed, tests, and archive packaging. Any change needs
a separate Task and matching evidence. This baseline intentionally passes all 20
tests; no scenario defect is seeded here.

P2-2 authors a candidate asset. P2-3 owns scenario-time canonical repository/version
selection and admission, scenario IDs/versions and allowlists, actual AISCC runs,
and Recorded Replay corpus/admission. This candidate does not enroll a security
profile, resource or scenario, authorize public Live, or start P2-3.
