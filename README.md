# Fernet Encryption Template

Minimal template for encrypting and decrypting secrets with a Fernet key.

This version keeps the database credential encrypted at rest and only decrypts it at runtime.

## Repository layout

```text
encryption-password/
├── .gitignore
├── db_executor.py
├── README.md
├── generate_key.py
└── requirements.txt
```

## What it does

- Generates a Fernet key
- Decrypts an encrypted database password before connecting
- Uses explicit CLI arguments instead of a fixed config file

## Manual upload flow

1. Copy the files into a GitLab repository.
2. Keep the encrypted password only in your local config file.
3. Run `python generate_key.py --output encryption.key`.
4. Use a one-off local command to encrypt the database password with the generated key, then paste the encrypted value into `housekeeping_config.ini`.
5. Run `python db_executor.py --config housekeeping_config.ini` to decrypt the database password at runtime.

## One-off encryption example

Use a temporary local command outside the repo to create the encrypted value once:

```powershell
python -c "from cryptography.fernet import Fernet; key = Fernet(open('encryption.key','rb').read()); print(key.encrypt(b'your_password_here').decode())"
```

