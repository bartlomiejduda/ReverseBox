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

**Who should use ReverseBox?** <br>
Mostly developers and reverse engineers (e.g. file format researchers
or software researchers).

# List of functionalities

* Checksum
  - CRC16 ✔️
  - CRC32 ✔️
  - CRC-16 (Modbus) (TODO) ❌
  - CRC-16 (Sick) (TODO) ❌
  - CRC-CCITT (XModem) (TODO) ❌ 
  - CRC-CCITT (0xFFFF) (TODO) ❌
  - CRC-CCITT (0x1D0F) (TODO) ❌
  - CRC-CCITT (Kermit) (TODO) ❌
  - CRC-DNP (TODO) ❌
  - 1 byte checksum (TODO) ❌

* Compression
  - BZIP2 (TODO) ❌
  - GZIP (TODO) ❌
  - JCALG1 (TODO) ❌
  - LZMA (TODO) ❌
  - LZO1X (TODO) ❌
  - LZSS (TODO) ❌
  - NitroSDK (TODO) ❌
  - Oodle (TODO) ❌
  - Refpack (EA) (TODO) ❌
  - RNC (TODO) ❌
  - ZLIB (TODO) ❌

* Encryption
  - AES (TODO) ❌
  - DES (TODO) ❌
  - XOR Cipher (Basic) ✔️
  - XOR Cipher (game-specific: Retro64 ECO) ✔️
  - XOR Cipher (game-specific: Giana’s Return ZDA) (TODO) ❌

* Hash
  - SHA-1 (TODO) ❌
  - MD5 (TODO) ❌
  - (game-specific) Hercules (TODO) ❌
  - (game-specific) E-racer (TODO) ❌

* IO
  - Basic IO operations (TODO) ❌

# Checksum calculation- example
Below is an example for checksum calculation using ReverseBox package.
Calulating other checksums is very similar.

// CRC16 calculation
```
from reversebox.checksum import checksum_crc16
from reversebox.common import common


test_data = b'123456789'
crc16_handler = checksum_crc16.CRC16Handler()
crc16 = crc16_handler.calculate_crc16(test_data)
print("CRC16_INT: ", crc16)
print("CRC16_STR: ", common.convert_int_to_hex_string(crc16))
```
// CRC16 output
```
CRC16_INT:  47933
CRC16_STR:  0xBB3D
```