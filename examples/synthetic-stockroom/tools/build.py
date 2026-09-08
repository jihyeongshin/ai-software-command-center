"""Deterministic development archive, not a sandbox or admission mechanism."""

from pathlib import Path
from zipfile import ZIP_STORED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
INPUTS = (
    "stockroom/__init__.py",
    "stockroom/__main__.py",
    "stockroom/cli.py",
    "stockroom/data/catalog.json",
    "stockroom/inventory.py",
    "stockroom/model.py",
)
LAUNCHER = b"from stockroom.cli import main\nraise SystemExit(main())\n"


def build() -> Path:
    payload = {"__main__.py": LAUNCHER}
    for name in INPUTS:
        source = ROOT / name
        if any(path.is_symlink() or path.is_junction() for path in (source, *source.parents) if path != ROOT.parent):
            raise ValueError("linked build input")
        payload[name] = source.read_bytes()
    directory = ROOT / ".build"
    destination = directory / "stockroom.pyz"
    if directory.is_symlink() or directory.is_junction() or destination.is_symlink() or destination.is_junction():
        raise ValueError("linked build output")
    directory.mkdir(exist_ok=True)
    with ZipFile(destination, "w", compression=ZIP_STORED) as archive:
        for name in sorted(payload):
            entry = ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.compress_type = ZIP_STORED
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            entry.internal_attr = 0
            entry.extra = b""
            entry.comment = b""
            archive.writestr(entry, payload[name])
    return destination


if __name__ == "__main__":
    build()
