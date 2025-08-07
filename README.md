# Simple Image Encryption Tool

A beginner-friendly Python tool for encrypting and decrypting images using **XOR pixel scrambling + position permutation**.  
Built for learning purposes — **not** for high-security use.

## Features

- Encrypts any image (JPEG, PNG, etc.)
- Fully reversible with the correct passphrase
- Uses XOR on RGB channels + pixel shuffling
- Works entirely offline

## Requirements

- Python 3
- Pillow library (`pip install pillow`)

## Usage

**Encrypt an image**
```bash
python3 imgcrypt.py encrypt input.jpg encrypted.png -k "my passphrase"

**Decrypt an image**

python3 imgcrypt.py decrypt encrypted.png output.png -k "my passphrase"

# Important: Always save encrypted images as PNG (lossless), otherwise decryption may fail.

## File Structure

image-encryptor/
├── imgcrypt.py    # Main encryption/decryption script
├── README.md      # Project documentation
├── .gitignore     # Ignore unnecessary files
└── LICENSE        # License file

## Example in Termux

python3 imgcrypt.py encrypt ~/storage/downloads/practice.jpg ~/storage/downloads/practice_encrypted.png -k "secret"
python3 imgcrypt.py decrypt ~/storage/downloads/practice_encrypted.png ~/storage/downloads/practice_decrypted.png -k "secret"

## Author

Godson Enruchi Chukwu
Intern (Prodigy InfoTech)

## License

This project is licensed under the MIT License — see LICENSE for details.
