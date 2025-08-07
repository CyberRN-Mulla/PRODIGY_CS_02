#!/usr/bin/env python3
"""
Simple image encrypt/decrypt using XOR + pixel permutation.
Usage:
  python3 imgcrypt.py encrypt  input.jpg output.png -k "my pass"
  python3 imgcrypt.py decrypt input.png output.png -k "my pass"
Notes:
 - Encrypted output SHOULD be saved as PNG (lossless). JPEG will break decryption.
 - The passphrase must be identical for encrypt and decrypt.
"""

import argparse, hashlib, random
from PIL import Image

def derive_seed_and_bytes(passphrase):
    h = hashlib.sha256(passphrase.encode('utf-8')).digest()  # 32 bytes
    seed = int.from_bytes(h[:8], 'big')  # use first 8 bytes for random seed
    return seed, h  # return full hash bytes for XOR stream

def xor_pixels(pixels, key_bytes):
    klen = len(key_bytes)
    out = []
    # apply XOR to R,G,B in repeated fashion using key_bytes
    for i, (r, g, b) in enumerate(pixels):
        rb = r ^ key_bytes[(3*i) % klen]
        gb = g ^ key_bytes[(3*i + 1) % klen]
        bb = b ^ key_bytes[(3*i + 2) % klen]
        out.append((rb, gb, bb))
    return out

def encrypt_image(in_path, out_path, passphrase):
    img = Image.open(in_path).convert('RGB')
    pixels = list(img.getdata())
    seed, key_bytes = derive_seed_and_bytes(passphrase)

    # Step 1: XOR each pixel's channels
    xored = xor_pixels(pixels, key_bytes)

    # Step 2: Permute pixel positions using seeded RNG
    indices = list(range(len(xored)))
    rng = random.Random(seed)
    rng.shuffle(indices)
    encrypted_pixels = [ xored[i] for i in indices ]

    out = Image.new('RGB', img.size)
    out.putdata(encrypted_pixels)
    out.save(out_path, format='PNG')
    print(f"[+] Encrypted -> {out_path}")

def decrypt_image(in_path, out_path, passphrase):
    img = Image.open(in_path).convert('RGB')
    pixels = list(img.getdata())
    seed, key_bytes = derive_seed_and_bytes(passphrase)

    # Recreate same permutation indices and invert it
    indices = list(range(len(pixels)))
    rng = random.Random(seed)
    rng.shuffle(indices)

    # inverse permutation: original[indices[j]] = pixels[j]
    original = [None] * len(pixels)
    for j, pix in enumerate(pixels):
        original[indices[j]] = pix

    # XOR again to recover original RGB (XOR is its own inverse)
    recovered = xor_pixels(original, key_bytes)

    out = Image.new('RGB', img.size)
    out.putdata(recovered)
    out.save(out_path, format='PNG')
    print(f"[+] Decrypted -> {out_path}")

def main():
    p = argparse.ArgumentParser(description="Simple image encrypt/decrypt (XOR + permute)")
    p.add_argument('mode', choices=['encrypt','decrypt'])
    p.add_argument('input', help='input image path')
    p.add_argument('output', help='output image path (use .png for safety)')
    p.add_argument('-k','--key', required=True, help='passphrase key (keep secret)')
    args = p.parse_args()

    if args.mode == 'encrypt':
        encrypt_image(args.input, args.output, args.key)
    else:
        decrypt_image(args.input, args.output, args.key)

if __name__ == '__main__':
    main()
