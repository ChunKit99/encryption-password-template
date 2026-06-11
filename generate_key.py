import argparse
from pathlib import Path

from cryptography.fernet import Fernet


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a Fernet key file.")
    parser.add_argument("--output", default="encryption.key")
    args = parser.parse_args()

    key_path = Path(args.output)
    key_path.write_bytes(Fernet.generate_key())
    print(f"Wrote key to {key_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
