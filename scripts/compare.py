#!/usr/bin/env python3
"""Compare a baseline and a candidate implementation on generated inputs.

Each implementation is a function that takes one input and returns a result.
The input generator is a function make_input(n, seed) that returns one input
of size n. Functions are given as path/to/file.py:name or package.module:name.

Example:
    python scripts/compare.py \\
        --baseline baseline.py:solve \\
        --candidate candidate.py:solve \\
        --inputs gen.py:make_input \\
        --sizes 0,1,100,10000,1000000

For each size it reports median and best wall time over the repeats, peak
memory allocated through Python during one call (tracemalloc), the speedup
of the candidate over the baseline, and whether the outputs agree.

Each call gets a fresh deep copy of the input, so an implementation that
mutates its input cannot affect the other or later repeats. Copying is not
included in the timings.

Exit status is 1 if any outputs disagree or the candidate raises or times
out. Baseline failures are reported in the table but do not fail the run.
"""

import argparse
import copy
import importlib
import importlib.util
import json
import os
import signal
import statistics
import sys
import time
import tracemalloc


class Timeout(Exception):
    pass


def load(spec):
    """Load a function from 'path/to/file.py:name' or 'package.module:name'."""
    if ":" not in spec:
        raise SystemExit(f"expected target:function, got {spec!r}")
    target, name = spec.rsplit(":", 1)
    if target.endswith(".py") or os.sep in target or "/" in target:
        path = os.path.abspath(target)
        if not os.path.isfile(path):
            raise SystemExit(f"file not found: {path}")
        mod_name = "_compare_" + os.path.splitext(os.path.basename(path))[0]
        mod_spec = importlib.util.spec_from_file_location(mod_name, path)
        if mod_spec is None or mod_spec.loader is None:
            raise SystemExit(f"cannot load {path}")
        module = importlib.util.module_from_spec(mod_spec)
        sys.path.insert(0, os.path.dirname(path))
        mod_spec.loader.exec_module(module)
    else:
        module = importlib.import_module(target)
    try:
        return getattr(module, name)
    except AttributeError:
        raise SystemExit(f"{target} has no attribute {name!r}")


def _on_alarm(signum, frame):
    raise Timeout()


def timed_call(fn, arg, timeout):
    """Call fn(arg) and return (result, seconds). Timeout needs SIGALRM (Unix)."""
    use_alarm = bool(timeout) and hasattr(signal, "SIGALRM")
    if use_alarm:
        signal.signal(signal.SIGALRM, _on_alarm)
        signal.setitimer(signal.ITIMER_REAL, timeout)
    try:
        start = time.perf_counter()
        result = fn(arg)
        elapsed = time.perf_counter() - start
    finally:
        if use_alarm:
            signal.setitimer(signal.ITIMER_REAL, 0)
    return result, elapsed


def measure(fn, inp, repeats, timeout):
    """Time fn over several fresh copies of inp, then measure peak memory once."""
    times = []
    result = None
    for _ in range(repeats):
        arg = copy.deepcopy(inp)
        result, elapsed = timed_call(fn, arg, timeout)
        times.append(elapsed)

    arg = copy.deepcopy(inp)
    tracemalloc.start()
    try:
        timed_call(fn, arg, timeout)
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    return result, times, peak


def default_equal(a, b):
    try:
        return bool(a == b)
    except (ValueError, TypeError):
        pass
    try:
        import numpy as np
    except ImportError:
        raise SystemExit("outputs cannot be compared with ==; pass --check")
    return bool(np.array_equal(a, b))


def fmt_time(seconds):
    if seconds is None:
        return "-"
    if seconds < 1e-3:
        return f"{seconds * 1e6:.1f} us"
    if seconds < 1:
        return f"{seconds * 1e3:.2f} ms"
    return f"{seconds:.3f} s"


def fmt_bytes(n):
    if n is None:
        return "-"
    for unit in ("B", "KiB", "MiB", "GiB"):
        if n < 1024 or unit == "GiB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024


def run_one(fn, inp, repeats, timeout):
    try:
        result, times, peak = measure(fn, inp, repeats, timeout)
    except Timeout:
        return None, {"status": "timeout"}
    except Exception as exc:  # report any failure of the code under test
        return None, {"status": f"error: {type(exc).__name__}: {exc}"}
    return result, {
        "status": "ok",
        "median_s": statistics.median(times),
        "best_s": min(times),
        "peak_bytes": peak,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Compare a baseline and a candidate implementation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--baseline", required=True, help="file.py:function")
    parser.add_argument("--candidate", required=True, help="file.py:function")
    parser.add_argument("--inputs", required=True,
                        help="file.py:function with signature make_input(n, seed)")
    parser.add_argument("--sizes", required=True,
                        help="comma-separated input sizes, e.g. 0,1,100,10000")
    parser.add_argument("--check",
                        help="file.py:function with signature check(inp, baseline_out, "
                             "candidate_out) -> bool; default compares with ==")
    parser.add_argument("--repeats", type=int, default=5,
                        help="timed runs per size (default 5)")
    parser.add_argument("--timeout", type=float, default=60.0,
                        help="seconds per call, 0 to disable (default 60; Unix only)")
    parser.add_argument("--seed", type=int, default=0, help="seed passed to make_input")
    parser.add_argument("--json", help="also write the results to this JSON file")
    args = parser.parse_args()

    baseline = load(args.baseline)
    candidate = load(args.candidate)
    make_input = load(args.inputs)
    check = load(args.check) if args.check else None
    sizes = [int(s) for s in args.sizes.split(",") if s.strip()]

    rows = []
    failed = False
    for n in sizes:
        inp = make_input(n, args.seed)
        base_out, base = run_one(baseline, inp, args.repeats, args.timeout)
        cand_out, cand = run_one(candidate, inp, args.repeats, args.timeout)

        if base["status"] == "ok" and cand["status"] == "ok":
            if check:
                agree = bool(check(copy.deepcopy(inp), base_out, cand_out))
            else:
                agree = default_equal(base_out, cand_out)
            outputs = "agree" if agree else "DISAGREE"
            failed |= not agree
        else:
            outputs = "not compared"
        if cand["status"] != "ok":
            failed = True

        speedup = None
        if base.get("median_s") and cand.get("median_s"):
            speedup = base["median_s"] / cand["median_s"]
        rows.append({"n": n, "baseline": base, "candidate": cand,
                     "speedup": speedup, "outputs": outputs})

    def cell(side, key, fmt):
        return fmt(side[key]) if side["status"] == "ok" else side["status"]

    print("| n | baseline median | candidate median | speedup | "
          "baseline peak | candidate peak | outputs |")
    print("|---|---|---|---|---|---|---|")
    for r in rows:
        b, c = r["baseline"], r["candidate"]
        speed = f"{r['speedup']:.3g}x" if r["speedup"] else "-"
        print(f"| {r['n']} | {cell(b, 'median_s', fmt_time)} | "
              f"{cell(c, 'median_s', fmt_time)} | {speed} | "
              f"{cell(b, 'peak_bytes', fmt_bytes)} | "
              f"{cell(c, 'peak_bytes', fmt_bytes)} | {r['outputs']} |")
    print(f"\nrepeats={args.repeats} seed={args.seed} python={sys.version.split()[0]}"
          "  speedup = baseline median / candidate median")

    if args.json:
        with open(args.json, "w") as fh:
            json.dump({"repeats": args.repeats, "seed": args.seed, "rows": rows},
                      fh, indent=2)

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
