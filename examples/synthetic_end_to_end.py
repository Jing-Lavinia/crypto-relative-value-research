from __future__ import annotations

import json

from perpetual_rv_demo import run_synthetic_pipeline


if __name__ == "__main__":
    print(json.dumps(run_synthetic_pipeline(), indent=2, sort_keys=True))

