# Info

**ReverseBox** is a Python package with a set of functions
useful in software reverse engineering.

**Why ReverseBox?** <br>
It's designed to help with: 
1. Decompressing / compressing data
2. Decrypting / encrypting data
3. Tedious reverse engineering tasks
e.g. testing different checksum algorithms to find the one that was
used in the software or file format.
4. Parsing data structures
5. Wrapping functions for input/output operations

**Who should use ReverseBox?** <br>
Mostly developers and reverse engineers (e.g. file format researchers
or software researchers).

# List of functionalities

* Checksum
  - CRC16 :heavy_check_mark:
  - CRC32 :heavy_check_mark:
  - CRC-16 (Modbus) (TODO) :x:
  - CRC-16 (Sick) (TODO) :x:
  - CRC-CCITT (XModem) (TODO) :x:
  - CRC-CCITT (0xFFFF) (TODO) :x:
  - CRC-CCITT (0x1D0F) (TODO) :x:
  - CRC-CCITT (Kermit) (TODO) :x:
  - CRC-DNP (TODO) :x:
  - 1 byte checksum :x:

* Compression
  - ZLIB (TODO) :x:
  - Refpack (TODO) :x:

* Encryption
  - Basic XOR (TODO) :x:

* Hash
  - MD5 (TODO) :x:

* IO
  - TODO

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