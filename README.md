# Info

**ReverseBox** is a Python package with a set of functions
useful in software reverse engineering.

**Why ReverseBox?** <br>
It's designed to help with:
1. Decompressing / compressing data
2. Decrypting / encrypting data
3. Tedious reverse engineering tasks
e.g. testing different checksum algorithms to find the one that was
used in the software or file format
4. Figuring out file formats
5. Parsing data structures
6. Wrapping functions for input/output operations
7. Searching for raw images

**Who should use ReverseBox?** <br>
Mostly developers and reverse engineers (e.g. file format researchers
or software researchers).

# List of functionalities

* Checksum/CRC
  - Adler-32 ✔️
  - CRC-8 (TODO) ❌
  - CRC-16 (ARC) ✔️
  - CRC-16 (Modbus) ✔️
  - CRC-16 (Sick) ✔️
  - CRC-16 (DNP) ✔️
  - CRC-16-CCITT (XModem) ✔️
  - CRC-16-CCITT (0xFFFF) ✔️
  - CRC-16-CCITT (0x1D0F) ✔️
  - CRC-16-CCITT (Kermit) ✔️
  - CRC-32 (ISO/HDLC) ✔️
  - CRC-32 (Asobo) (TODO) ❌

* Compression
  - Asobo (TODO) ❌
  - BZE/BZZ (TODO) ❌
  - BZIP2 (TODO) ❌
  - GZIP (TODO) ❌
  - JCALG1 (TODO) ❌
  - LZMA (TODO) ❌
  - LZO / LZO1X ✔️ <span style="color:yellow">(wrapper only)</span>
  - LZSS (TODO) ❌
  - NitroSDK (TODO) ❌
  - Oodle (TODO) ❌
  - Refpack (EA) (TODO) ❌
  - RNC (TODO) ❌
  - ZLIB ✔️ <span style="color:yellow">(wrapper only)</span>

* Encryption
  - AES (TODO) ❌
  - DES (TODO) ❌
  - Lucifer / DTD-1 (TODO) ❌
  - XOR Cipher (Basic) ✔️
  - (game-specific) XOR Cipher (Retro64 ECO) ✔️
  - (game-specific) XOR Cipher (Giana’s Return ZDA) (TODO) ❌

* Hash
  - SHA-1 ✔️ <span style="color:yellow">(wrapper only)</span>
  - SHA-2 (256 bits) ✔️ <span style="color:yellow">(wrapper only)</span>
  - MD5 ✔️ <span style="color:yellow">(wrapper only)</span>
  - (game-specific) Hercules (TODO) ❌
  - (game-specific) E-racer (TODO) ❌

* Image
  - Image Finder  (in progress) ❌
  - PS2 Swizzling/Twiddling (TODO) ❌
  - PSP Swizzling/Twiddling (TODO) ❌

* IO
  - File Reader ✔️
  - File Writer ✔️
  - Bytes Handler ✔️
  - File extension checking ✔️

# Checksum calculation - example

// CRC32 calculation
```
from reversebox.checksum import checksum_crc32_iso_hdlc
from reversebox.common import common

test_data = b'123456789'
crc32_handler = checksum_crc32_iso_hdlc.CRC32Handler()
crc32 = crc32_handler.calculate_crc32(test_data)
print("CRC32_INT: ", crc32)
print("CRC32_STR: ", common.convert_int_to_hex_string(crc32))
```
// CRC32 output
```
CRC32_INT:  3421780262
CRC32_STR:  0xCBF43926
```


# XOR encryption - example

// XOR Cipher (Basic)
```
from reversebox.encryption.encryption_xor_basic import xor_cipher_basic


test_data = b'abcd'
test_key = b'\x3D'
xor_result = xor_cipher_basic(test_data, test_key)
print(xor_result)
```

// XOR Cipher output
```
b'\\_^Y'
```


# File Handler - example

// File reading
```
from reversebox.io_files.file_handler import FileHandler


file_path = os.path.join(os.path.dirname(__file__), "file.bin")
file_reader = FileHandler(file_path, "rb")
file_reader.open()
value = file_reader.read_str(4, "utf8")
print(value)
```

// File Reader Output
```
ABCD
```


# Hash calculation - example

// SHA-1 calculation
```
from reversebox.hash.hash_sha1 import SHA1Handler

test_data = b'abcd'
sha1_handler = SHA1Handler()
sha1 = sha1_handler.calculate_sha1_hash(test_data)
print("SHA-1 hash: ", sha1)
```

// SHA-1 Output
```
SHA-1 hash:  b'\x81\xfe\x8b\xfe\x87Wl>\xcb"Bo\x8eW\x84s\x82\x91z\xcf'
```
