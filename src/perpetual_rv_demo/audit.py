from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def stable_hash(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def write_immutable_record(path: str | Path, payload: dict) -> None:
    """Write one audit record and reject accidental replacement."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    record = {**payload, "payload_sha256": stable_hash(payload)}
    with destination.open("x", encoding="utf-8") as handle:
        json.dump(record, handle, indent=2, sort_keys=True)
        handle.write("\n")

