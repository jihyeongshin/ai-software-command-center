import ast
import hashlib
import json
import runpy
import sys
import unittest
from pathlib import Path
from zipfile import ZIP_STORED, ZipFile

from stockroom.inventory import decode_catalog
from stockroom.model import StockroomError


ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "README.md", "PROVENANCE.md", ".python-version", ".gitignore",
    "stockroom/__init__.py", "stockroom/__main__.py", "stockroom/model.py",
    "stockroom/inventory.py", "stockroom/cli.py", "stockroom/data/catalog.json",
    "tests/test_inventory.py", "tests/test_cli.py", "tests/test_contract.py", "tools/build.py",
}
PAYLOAD = {
    "__main__.py", "stockroom/__init__.py", "stockroom/__main__.py",
    "stockroom/model.py", "stockroom/inventory.py", "stockroom/cli.py",
    "stockroom/data/catalog.json",
}


def build():
    return runpy.run_path(str(ROOT / "tools/build.py"), run_name="stockroom_build_test")["build"]()


def source_hashes():
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in sorted(SOURCES)}


class ContractTests(unittest.TestCase):
    def test_exact_source_inventory(self):
        actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file()}
        self.assertEqual(actual - {".build/stockroom.pyz"}, SOURCES)
        self.assertEqual(len(SOURCES), 14)
        self.assertEqual((ROOT / ".gitignore").read_bytes(), b".build/\n__pycache__/\n")
        self.assertEqual({p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_dir()},
                         {"stockroom", "stockroom/data", "tests", "tools"} |
                         ({".build"} if (ROOT / ".build").exists() else set()))

    def test_python_pin_and_stdlib_imports(self):
        self.assertEqual(sys.implementation.name, "cpython")
        self.assertEqual(sys.version_info[:3], (3, 12, 14))
        self.assertEqual((ROOT / ".python-version").read_bytes(), b"3.12.14\n")
        forbidden_runtime = {"socket", "subprocess", "http", "urllib", "sqlite3", "ctypes", "aiscc"}
        for name in sorted(SOURCES):
            if not name.endswith(".py"):
                continue
            tree = ast.parse((ROOT / name).read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                modules = []
                if isinstance(node, ast.Import):
                    modules = [alias.name.split(".")[0] for alias in node.names]
                elif isinstance(node, ast.ImportFrom) and node.level == 0:
                    modules = [node.module.split(".")[0]]
                for module in modules:
                    self.assertIn(module, sys.stdlib_module_names | {"stockroom"}, (name, module))
                    self.assertNotEqual(module, "aiscc")
                    if name.startswith("stockroom/"):
                        self.assertNotIn(module, forbidden_runtime)
                if name.startswith("stockroom/") and isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    self.assertNotIn(node.func.id, {"eval", "exec", "__import__"})

    def test_seed_schema_and_size(self):
        data = (ROOT / "stockroom/data/catalog.json").read_bytes()
        self.assertLessEqual(len(data), 4096)
        self.assertEqual(json.loads(data), [
            {"sku": "BOX-A", "on_hand": 12, "reserved": 2, "reorder_level": 3},
            {"sku": "BOX-B", "on_hand": 5, "reserved": 5, "reorder_level": 2},
            {"sku": "BOX-C", "on_hand": 4, "reserved": 1, "reorder_level": 3},
        ])
        bad_records = [b"[]", b"{}", b"null", b"[{}]", b"\xff", b"[",
                       b'[{"sku":"X","sku":"Y","on_hand":1,"reserved":0,"reorder_level":0}]',
                       json.dumps([json.loads(data)[0]] * 2).encode()]
        extra = json.loads(data)
        extra[0]["extra"] = 0
        bad_records.append(json.dumps(extra).encode())
        for invalid in bad_records:
            with self.subTest(invalid=invalid[:30]), self.assertRaises(StockroomError):
                decode_catalog(invalid)

    def test_no_links_nested_git_or_private_assets(self):
        for path in (ROOT, *ROOT.rglob("*")):
            self.assertFalse(path.is_symlink() or path.is_junction(), str(path))
            self.assertNotIn(path.name.lower(), {".git", ".env", ".ssh", "credentials", "__pycache__"})
            if path.is_file():
                self.assertIn(path.relative_to(ROOT).as_posix(), SOURCES | {".build/stockroom.pyz"})
        self.assertIn("license review remain pending", (ROOT / "PROVENANCE.md").read_text(encoding="utf-8"))

    def test_build_reproducible(self):
        before = source_hashes()
        first = build().read_bytes()
        second = build().read_bytes()
        self.assertEqual(first, second)
        self.assertEqual(hashlib.sha256(first).digest(), hashlib.sha256(second).digest())
        self.assertEqual(source_hashes(), before)

    def test_archive_entries_and_metadata(self):
        with ZipFile(build()) as archive:
            self.assertEqual(archive.namelist(), sorted(PAYLOAD))
            self.assertEqual(archive.comment, b"")
            self.assertEqual(archive.read("__main__.py"), b"from stockroom.cli import main\nraise SystemExit(main())\n")
            for entry in archive.infolist():
                self.assertEqual(entry.date_time, (1980, 1, 1, 0, 0, 0))
                self.assertEqual(entry.compress_type, ZIP_STORED)
                self.assertEqual(entry.create_system, 3)
                self.assertEqual(entry.external_attr, 0o100644 << 16)
                self.assertEqual(entry.internal_attr, 0)
                self.assertEqual(entry.flag_bits, 0)
                self.assertEqual((entry.extra, entry.comment), (b"", b""))
                self.assertFalse(entry.filename.startswith("/") or ":" in entry.filename or "\\" in entry.filename)
                if entry.filename != "__main__.py":
                    self.assertEqual(archive.read(entry), (ROOT / entry.filename).read_bytes())
