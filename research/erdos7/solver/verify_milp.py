"""Run exact MILP deficiencies as an independent check for the certificates."""

from __future__ import annotations

import json
import sys
import time

from milp import max_coverage_milp


def main(nums: list[int], out_path: str | None = None) -> None:
    results: dict[str, dict] = {}
    for N in nums:
        t0 = time.time()
        covered, delta = max_coverage_milp(N)
        dt = time.time() - t0
        results[str(N)] = {"N": N, "r": covered, "delta": delta, "seconds": round(dt, 3)}
        print(f"N={N} r={covered} delta={delta} {dt:.2f}s", flush=True)
    if out_path:
        with open(out_path, "w") as f:
            json.dump(results, f, indent=2)


if __name__ == "__main__":
    args = sys.argv[1:]
    out = args[-1] if args and args[-1].endswith(".json") else None
    num_args = args[:-1] if out else args
    nums = [int(x) for x in num_args]
    main(nums, out)
