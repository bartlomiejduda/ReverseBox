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
  - Adler32 ✔️
  - Fletcher16 ✔️
  - Fletcher32 ✔️
  - Internet Checksum / IPv4 header checksum ✔️
  - Sum8 ✔️
  - Sum8 2s Complement ✔️
  - Unix Sum BSD16 ✔️
  - Unix Sum SYSV ✔️
  - Xor8 ✔️

* CRC
  - CRC-8 ✔️
  - CRC-8/CDMA2000 ✔️
  - CRC-8/DARC ✔️ <span style="color:yellow">(wrapper only)</span>
  - CRC-16 (ARC) ✔️
  - CRC-16 (Modbus) ✔️
  - CRC-16 (Sick) ✔️
  - CRC-16 (DNP) ✔️
  - CRC-16 (EA CRCF) ✔️
  - CRC-16-CCITT (XModem) ✔️
  - CRC-16-CCITT (0xFFFF) ✔️
  - CRC-16-CCITT (0x1D0F) ✔️
  - CRC-16-CCITT (Kermit) ✔️
  - CRC-32/CKSUM (Unix cksum) ✔️
  - CRC-32 (ISO/HDLC) ✔️
  - CRC-32 (Asobo) ✔️
  - CRC-64 (Asobo) ✔️
  - CRC-64/GO-ISO ✔️ <span style="color:yellow">(wrapper only)</span>

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
  - Refpack (EA Games) ✔️ <span style="color:yellow">(wrapper only)</span>
  - RNC (TODO) ❌
  - ZLIB ✔️ <span style="color:yellow">(wrapper only)</span>

* Encryption
  - AES (TODO) ❌
  - DES (TODO) ❌
  - Lucifer / DTD-1 (TODO) ❌
  - ROT13 ✔️
  - XOR Cipher (Basic) ✔️
  - XOR Cipher (Basic) Guesser ✔️
  - (game-specific) XOR Cipher (Retro64 ECO) ✔️
  - (game-specific) XOR Cipher (Giana’s Return ZDA) ✔️

* Hash
  - DJB2 ✔️
  - FNV0-32 ✔️
  - FNV0-64 ✔️
  - FNV1-32 ✔️
  - FNV1-64 ✔️
  - FNV1A-32 ✔️
  - FNV1A-64 ✔️
  - SHA-1 ✔️ <span style="color:yellow">(wrapper only)</span>
  - SHA-2 (256 bits) ✔️ <span style="color:yellow">(wrapper only)</span>
  - MD2 ✔️ <span style="color:yellow">(wrapper only)</span>
  - MD5 ✔️ <span style="color:yellow">(wrapper only)</span>
  - (game-specific) Hercules (TODO) ❌
  - (game-specific) E-racer (TODO) ❌

* Image
  - Decode RGBA2222 ✔️
  - Decode RGBX2222 ✔️
  - Decode RGB565 ✔️
  - Decode RGB888 ✔️
  - Decode ARGB4444 ✔️
  - Decode RGBA4444 ✔️
  - Decode XRGB1555 ✔️
  - Decode ABGR1555 ✔️
  - Decode XBGR1555 ✔️
  - Decode ARGB8888 ✔️
  - Decode ABGR8888 ✔️
  - Decode PAL4_RGBX5551 ✔️
  - Decode PAL4_RGB888 ✔️
  - Decode PAL4_RGB565 ✔️
  - Decode PAL4_RGBA8888 ✔️
  - Decode PAL8_RGBX2222 ✔️
  - Decode PAL8_RGBX5551 ✔️
  - Decode PAL8_BGRX5551 ✔️
  - Decode PAL8_RGB888 ✔️
  - Decode PAL8_BGR888 ✔️
  - Decode PAL8_RGB565 ✔️
  - Decode PAL8_RGBX6666 ✔️
  - Decode PAL8_RGB5A3 ✔️
  - Decode PAL8_RGBA8888 ✔️
  - Decode PAL8_BGRA8888 ✔️
  - Decode DXT1 ✔️
  - Decode DXT3 ✔️
  - Decode DXT5 ✔️
  - Decode GST121 ✔️
  - Decode GST221 ✔️
  - Decode GST421 ✔️
  - Decode GST821 ✔️
  - Decode GST122 ✔️
  - Decode GST222 ✔️
  - Decode GST422 ✔️
  - Decode GST822 ✔️
  - Decode YUY2 ✔️
  - 3DS Swizzling/Twiddling ✔️
  - CMPR Swizzling/Twiddling ✔️
  - PS2 Swizzling/Twiddling ✔️
  - PSP Swizzling/Twiddling ✔️
  - GameCube/WII Swizzling/Twiddling ✔️
  - PSVITA Swizzling/Twiddling ✔️
  - Switch Swizzling/Twiddling ✔️
  - XBOX/PS3 Swizzling/Twiddling (Morton Order) ✔️
  - PS2 GS Texture Swizzling/Twiddling ✔️
  - PS2 GS Texture Compression ✔️

* IO
  - File Reader ✔️
  - File Writer ✔️
  - Bytes Handler ✔️
  - Translation Text Handler ✔️
  - Mod Handler ✔️
  - File extension checking ✔️
  - Padding calculation ✔️
  - File size checking ✔️

# Checksum calculation - example

// CRC32 calculation
```
from reversebox.crc import crc32_iso_hdlc
from reversebox.common import common

test_data = b'123456789'
crc32_handler = crc32_iso_hdlc.CRC32Handler()
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
import os
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

# More Examples

Need more examples? <br>
Check out list of tools written using ReverseBox:
- [Giana's Return ZDA Tool](https://github.com/bartlomiejduda/Tools/blob/master/NEW%20Tools/Gianas%20Return/Gianas_Return_ZDA_Tool.py)
- [ObsCure 2 HVP Extractor](https://github.com/bartlomiejduda/Tools/blob/master/NEW%20Tools/ObsCure%202/ObsCure%202%20HVP%20Tools/Obscure_2_hvp_extractor.py)
- [Tail Concerto Translation Tools](https://github.com/bartlomiejduda/Tools/tree/master/NEW%20Tools/Tail%20Concerto/Tail%20Concerto%20Tools)
- [EA Graphics Manager](https://github.com/bartlomiejduda/EA-Graphics-Manager)
- and more...
