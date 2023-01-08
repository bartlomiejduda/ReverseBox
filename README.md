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

* Checksum
  - CRC8 (TODO) ❌
  - CRC16 (ARC) ✔️
  - CRC16 (Modbus) ✔️
  - CRC16 (Sick) ✔️
  - CRC16 (DNP) ✔️
  - CRC16-CCITT (XModem) ✔️
  - CRC16-CCITT (0xFFFF) ✔️
  - CRC16-CCITT (0x1D0F) ✔️
  - CRC16-CCITT (Kermit) ✔️
  - CRC32 (ISO/HDLC) ✔️
  - CRC32 (Asobo) (TODO) ❌

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

// CRC16 (Kermit) calculation
```
from reversebox.checksum import checksum_crc16_kermit
from reversebox.common import common

test_data = b'123456789'
crc16_handler = checksum_crc16_kermit.CRC16KermitHandler()
crc16 = crc16_handler.calculate_crc16_kermit(test_data)
print("CRC16_INT: ", crc16)
print("CRC16_STR: ", common.convert_int_to_hex_string(crc16))
```
// CRC16 (Kermit) output
```
CRC16_INT:  35105
CRC16_STR:  0x8921
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
