from __future__ import annotations

import json
import os
from pathlib import Path

status = Path("/proc/self/status").read_text(encoding="utf-8").splitlines()
uid = int(next(line for line in status if line.startswith("Uid:")).split()[1])
gid = int(next(line for line in status if line.startswith("Gid:")).split()[1])

payload = {
    "uid": uid,
    "gid": gid,
    "input": Path("/workspace/input.txt").read_text(encoding="utf-8").strip(),
    "workspace_writable": os.access("/workspace", os.W_OK),
    "host_git_visible": Path("/workspace/../.git").exists(),
    "tmp_writable": os.access("/tmp", os.W_OK),
}
print(json.dumps(payload, sort_keys=True))
