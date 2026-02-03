#!/usr/bin/env python3
"""
A small, O(1)-memory implementation of `cat`.
- Streams bytes in fixed-size chunks (no full-file reads).
- Supports: cat.py [FILE ...] and "-" for stdin.
- Exits cleanly on BrokenPipeError (e.g., piped to head).
"""
import sys

BUF_SIZE = 1024 * 1024  # 1 MiB

def stream_copy(src, dst) -> None:
    while True:
        chunk = src.read(BUF_SIZE)
        if not chunk:
            return
        dst.write(chunk)

def main(argv: list[str]) -> int:
    out = sys.stdout.buffer
    try:
        if len(argv) == 0:
            stream_copy(sys.stdin.buffer, out)
            return 0

        for path in argv:
            if path == "-":
                stream_copy(sys.stdin.buffer, out)
                continue
            try:
                with open(path, "rb") as f:
                    stream_copy(f, out)
            except FileNotFoundError:
                print(f"cat.py: {path}: No such file or directory", file=sys.stderr)
                return 1
            except PermissionError:
                print(f"cat.py: {path}: Permission denied", file=sys.stderr)
                return 1

        return 0

    except BrokenPipeError:
        # Downstream closed early; match standard Unix behavior (no traceback).
        try:
            sys.stdout.close()
        except Exception:
            pass
        return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
