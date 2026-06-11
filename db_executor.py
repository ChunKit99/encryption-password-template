import argparse
import configparser
from pathlib import Path

import mysql.connector
from cryptography.fernet import Fernet, InvalidToken


def load_key(path: Path) -> Fernet:
    return Fernet(path.read_bytes())


def decrypt_password(cipher: Fernet, encrypted_password: str) -> str:
    try:
        return cipher.decrypt(encrypted_password.encode("utf-8")).decode("utf-8")
    except InvalidToken as exc:
        raise SystemExit("Failed to decrypt database password with the provided key") from exc


def read_config(path: Path) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    if not path.is_file():
        raise SystemExit(f"Configuration file not found: {path}")
    config.read(path)
    return config


def main() -> int:
    parser = argparse.ArgumentParser(description="Connect to MySQL using an encrypted database password.")
    parser.add_argument("--config", default="housekeeping_config.ini")
    parser.add_argument("--key", default="encryption.key")
    args = parser.parse_args()

    config = read_config(Path(args.config))
    cipher = load_key(Path(args.key))

    database_user = config.get("database", "user")
    encrypted_database_password = config.get("database", "encrypted_password")
    database_name = config.get("database", "name")
    database_host = config.get("database", "host", fallback="localhost")
    database_port = config.getint("database", "port", fallback=3306)

    database_password = decrypt_password(cipher, encrypted_database_password)
    connection = mysql.connector.connect(
        user=database_user,
        password=database_password,
        database=database_name,
        host=database_host,
        port=database_port,
    )

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print(cursor.fetchone())
        cursor.close()
    finally:
        connection.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
