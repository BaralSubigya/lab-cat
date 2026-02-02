'''
This program prints stdin to the screen.
'''
import sys

def main() -> None:
    inp = sys.stdin.buffer
    out = sys.stdout.buffer

    while True:
        chunk = inp.read(1024 * 1024)  # 1 MiB
        if not chunk:
            break
        out.write(chunk)

if __name__ == "__main__":
    main()
)
