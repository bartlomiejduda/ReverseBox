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
  - Cocos2d PVR ✔️
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
  - BZIP2 ✔️ <span style="color:yellow">(wrapper only)</span>
  - GZIP (TODO) ❌
  - JCALG1 (TODO) ❌
  - LZ4 ✔️ <span style="color:yellow">(wrapper only)</span>
  - LZMA ✔️ <span style="color:yellow">(wrapper only)</span>
  - LZO / LZO1X ✔️ <span style="color:yellow">(wrapper only)</span>
  - LZSS (TODO) ❌
  - MIO0 ✔️
  - NitroSDK (TODO) ❌
  - Oodle (TODO) ❌
  - Refpack (EA Games) ✔️ <span style="color:yellow">(wrapper only)</span>
  - RNC (TODO) ❌
  - ZLIB ✔️ <span style="color:yellow">(wrapper only)</span>
  - PS2 GS Texture Compression ✔️
  - RLE TGA ✔️
  - RLE TGA (reversed condition) ✔️
  - PackBits (Macintosh RLE) ✔️
  - (game-specific) Re:Tiyoruga DAT compression ✔️
  - (game-specific) Intelligent Games Custom Huffman ✔️
  - (game-specific) Executioners RLE ✔️
  - (game-specific) Emergency RLE ✔️
  - (game-specific) Neversoft RLE ✔️
  - (game-specific) Tzar RLE ✔️
  - (game-specific) Leapster RLE ✔️

* Encryption
  - AES (TODO) ❌
  - DES (TODO) ❌
  - Lucifer / DTD-1 (TODO) ❌
  - ROT13 ✔️
  - XOR Cipher (Basic) ✔️
  - XOR Cipher (Basic) Guesser ✔️
  - Hatch Engine Encryption ✔️
  - (game-specific) XOR Cipher (Retro64 ECO) ✔️
  - (game-specific) XOR Cipher (Giana’s Return ZDA) ✔️

* Hash
  - Additive Hash ✔️
  - AP ✔️
  - DJB2 ✔️
  - RX3 ✔️
  - FNV0-32 ✔️
  - FNV0-64 ✔️
  - FNV1-32 ✔️
  - FNV1-64 ✔️
  - FNV1A-32 ✔️
  - FNV1A-64 ✔️
  - Jenkins one-at-a-time ✔️
  - SDBM ✔️
  - SHA-1 ✔️ <span style="color:yellow">(wrapper only)</span>
  - SHA-2 (256 bits) ✔️ <span style="color:yellow">(wrapper only)</span>
  - MD2 ✔️ <span style="color:yellow">(wrapper only)</span>
  - MD5 ✔️ <span style="color:yellow">(wrapper only)</span>
  - Murmur3 ✔️ <span style="color:yellow">(wrapper only)</span>
  - (game-specific) Hercules (TODO) ❌
  - (game-specific) E-racer (TODO) ❌
  - (game-specific) Pivotal Games DAT Hash ✔️

* Image
  - 3DS Swizzling/Twiddling ✔️
  - CMPR Swizzling/Twiddling ✔️
  - PS2 Swizzling/Twiddling ✔️
  - PS2 Palette Swizzling/Twiddling ✔️
  - PS4 Swizzling/Twiddling ✔️
  - PSP Swizzling/Twiddling ✔️
  - PS Vita Swizzling/Twiddling ✔️
  - XBOX 360 Swizzling/Twiddling ✔️
  - GameCube/WII Swizzling/Twiddling ✔️
  - Switch Swizzling/Twiddling ✔️
  - WII U Swizzling/Twiddling ✔️
  - XBOX/PS3 Swizzling/Twiddling (Morton Order) ✔️
  - Dreamcast Swizzling/Twiddling (Morton Order) ✔️
  - BC Swizzling/Twiddling ✔️
  - PS2 GS Texture Swizzling/Twiddling ✔️
  - Generating mipmaps ✔️
  - Decoding and encoding images with pixel formats <br>mentioned in the following table:

| Pixel Format           | Decode support      | Encode support      |
|------------------------|---------------------|---------------------|
| RGB121                 | <center>✔️</center> | <center>❌</center>  |
| ALPHA4                 | <center>✔️</center> | <center>❌</center>  |
| ALPHA4_16X             | <center>✔️</center> | <center>❌</center>  |
| RGB121_BYTE            | <center>✔️</center> | <center>❌</center>  |
| RGBA2222               | <center>✔️</center> | <center>❌</center>  |
| RGBX2222               | <center>✔️</center> | <center>❌</center>  |
| GRAY8                  | <center>✔️</center> | <center>❌</center>  |
| ALPHA8                 | <center>✔️</center> | <center>❌</center>  |
| ALPHA8_16X             | <center>✔️</center> | <center>❌</center>  |
| LA44                   | <center>✔️</center> | <center>❌</center>  |
| RGBX332 (RGB8)         | <center>✔️</center> | <center>❌</center>  |
| BGRX332 (BGR8)         | <center>✔️</center> | <center>❌</center>  |
| RGB565                 | <center>✔️</center> | <center>✔️</center> |
| BGR565                 | <center>✔️</center> | <center>✔️</center> |
| RGBX5551               | <center>✔️</center> | <center>✔️</center> |
| RGBT5551               | <center>✔️</center> | <center>✔️</center> |
| BGRT5551               | <center>✔️</center> | <center>✔️</center> |
| RGBA5551               | <center>✔️</center> | <center>✔️</center> |
| BGRA5551               | <center>✔️</center> | <center>✔️</center> |
| BGRA5551_TZAR          | <center>✔️</center> | <center>❌</center>  |
| BGRX5551               | <center>✔️</center> | <center>❌</center>  |
| RGBX6666               | <center>✔️</center> | <center>❌</center>  |
| RGBA6666               | <center>✔️</center> | <center>❌</center>  |
| RGB888 (RGB24)         | <center>✔️</center> | <center>✔️</center> |
| BGR888 (BGR24)         | <center>✔️</center> | <center>✔️</center> |
| ARGB4444               | <center>✔️</center> | <center>❌</center>  |
| RGBA4444               | <center>✔️</center> | <center>❌</center>  |
| ABGR4444               | <center>✔️</center> | <center>✔️</center> |
| XBGR4444               | <center>✔️</center> | <center>❌</center>  |
| RGBX4444               | <center>✔️</center> | <center>✔️</center> |
| BGRA4444               | <center>✔️</center> | <center>✔️</center> |
| BGRA4444_LEAPSTER      | <center>✔️</center> | <center>❌</center>  |
| BGRX4444               | <center>✔️</center> | <center>❌</center>  |
| XRGB1555               | <center>✔️</center> | <center>❌</center>  |
| ARGB1555               | <center>✔️</center> | <center>❌</center>  |
| ABGR1555               | <center>✔️</center> | <center>❌</center>  |
| XBGR1555               | <center>✔️</center> | <center>❌</center>  |
| ARGB8888               | <center>✔️</center> | <center>✔️</center> |
| ABGR8888               | <center>✔️</center> | <center>❌</center>  |
| RGBA8888               | <center>✔️</center> | <center>✔️</center> |
| BGRA8888               | <center>✔️</center> | <center>✔️</center> |
| XRGB8888               | <center>✔️</center> | <center>❌</center>  |
| RGBX8888               | <center>✔️</center> | <center>❌</center>  |
| XBGR8888               | <center>✔️</center> | <center>❌</center>  |
| BGRX8888               | <center>✔️</center> | <center>❌</center>  |
| BGRT8888               | <center>✔️</center> | <center>❌</center>  |
| BGRA8888_TZAR          | <center>✔️</center> | <center>❌</center>  |
| RGB48                  | <center>✔️</center> | <center>❌</center>  |
| BGR48                  | <center>✔️</center> | <center>❌</center>  |
| PAL4                   | <center>✔️</center> | <center>✔️</center> |
| PAL8                   | <center>✔️</center> | <center>✔️</center> |
| PAL8_TZAR              | <center>✔️</center> | <center>❌</center>  |
| PAL16                  | <center>✔️</center> | <center>❌</center>  |
| PAL32                  | <center>✔️</center> | <center>❌</center>  |
| PAL_I8A8               | <center>✔️</center> | <center>❌</center>  |
| N64_RGB5A3             | <center>✔️</center> | <center>❌</center>  |
| N64_I4                 | <center>✔️</center> | <center>❌</center>  |
| N64_I8                 | <center>✔️</center> | <center>❌</center>  |
| N64_IA4                | <center>✔️</center> | <center>❌</center>  |
| N64_IA8                | <center>✔️</center> | <center>❌</center>  |
| N64_RGBA32             | <center>✔️</center> | <center>❌</center>  |
| N64_CMPR               | <center>✔️</center> | <center>❌</center>  |
| BC1/DXT1               | <center>✔️</center> | <center>✔️</center> |
| PSP_DXT1               | <center>✔️</center> | <center>❌</center>  |
| DXT2                   | <center>✔️</center> | <center>❌</center>  |
| BC2/DXT3               | <center>✔️</center> | <center>✔️</center> |
| PSP_DXT3               | <center>✔️</center> | <center>❌</center>  |
| DXT4                   | <center>✔️</center> | <center>✔️</center> |
| BC3/DXT5               | <center>✔️</center> | <center>✔️</center> |
| PSP_DXT5               | <center>✔️</center> | <center>❌</center>  |
| BC4                    | <center>✔️</center> | <center>✔️</center> |
| BC5                    | <center>✔️</center> | <center>✔️</center> |
| BC6                    | <center>✔️</center> | <center>✔️</center> |
| BC7                    | <center>✔️</center> | <center>✔️</center> |
| PVRTCI_2bpp_RGB        | <center>✔️</center> | <center>✔️</center> |
| PVRTCI_2bpp_RGBA       | <center>✔️</center> | <center>✔️</center> |
| PVRTCI_4bpp_RGB        | <center>✔️</center> | <center>✔️</center> |
| PVRTCI_4bpp_RGBA       | <center>✔️</center> | <center>✔️</center> |
| PVRTCII_2bpp           | <center>✔️</center> | <center>✔️</center> |
| PVRTCII_4bpp           | <center>✔️</center> | <center>✔️</center> |
| ETC1                   | <center>✔️</center> | <center>✔️</center> |
| BW1bpp                 | <center>✔️</center> | <center>✔️</center> |
| SharedExponentR9G9B9E5 | <center>✔️</center> | <center>✔️</center> |
| RGBG8888               | <center>✔️</center> | <center>✔️</center> |
| GRGB8888               | <center>✔️</center> | <center>✔️</center> |
| ETC2_RGB               | <center>✔️</center> | <center>✔️</center> |
| ETC2_RGBA              | <center>✔️</center> | <center>✔️</center> |
| ETC2_RGB_A1            | <center>✔️</center> | <center>✔️</center> |
| EAC_R11                | <center>✔️</center> | <center>✔️</center> |
| EAC_RG11               | <center>✔️</center> | <center>✔️</center> |
| ASTC_4x4               | <center>✔️</center> | <center>✔️</center> |
| ASTC_5x4               | <center>✔️</center> | <center>✔️</center> |
| ASTC_5x5               | <center>✔️</center> | <center>✔️</center> |
| ASTC_6x5               | <center>✔️</center> | <center>✔️</center> |
| ASTC_6x6               | <center>✔️</center> | <center>✔️</center> |
| ASTC_8x5               | <center>✔️</center> | <center>✔️</center> |
| ASTC_8x6               | <center>✔️</center> | <center>✔️</center> |
| ASTC_8x8               | <center>✔️</center> | <center>✔️</center> |
| ASTC_10x5              | <center>✔️</center> | <center>✔️</center> |
| ASTC_10x6              | <center>✔️</center> | <center>✔️</center> |
| ASTC_10x8              | <center>✔️</center> | <center>✔️</center> |
| ASTC_10x10             | <center>✔️</center> | <center>✔️</center> |
| ASTC_12x10             | <center>✔️</center> | <center>✔️</center> |
| ASTC_12x12             | <center>✔️</center> | <center>✔️</center> |
| ASTC_3x3x3             | <center>✔️</center> | <center>✔️</center> |
| ASTC_4x3x3             | <center>✔️</center> | <center>✔️</center> |
| ASTC_4x4x3             | <center>✔️</center> | <center>✔️</center> |
| ASTC_4x4x4             | <center>✔️</center> | <center>✔️</center> |
| ASTC_5x4x4             | <center>✔️</center> | <center>✔️</center> |
| ASTC_5x5x4             | <center>✔️</center> | <center>✔️</center> |
| ASTC_5x5x5             | <center>✔️</center> | <center>✔️</center> |
| ASTC_6x5x5             | <center>✔️</center> | <center>✔️</center> |
| ASTC_6x6x5             | <center>✔️</center> | <center>✔️</center> |
| ASTC_6x6x6             | <center>✔️</center> | <center>✔️</center> |
| BASISU_ETC1S           | <center>✔️</center> | <center>✔️</center> |
| BASISU_UASTC           | <center>✔️</center> | <center>✔️</center> |
| RGBM                   | <center>✔️</center> | <center>✔️</center> |
| RGBD                   | <center>✔️</center> | <center>✔️</center> |
| GST121                 | <center>✔️</center> | <center>❌</center>  |
| GST221                 | <center>✔️</center> | <center>❌</center>  |
| GST421                 | <center>✔️</center> | <center>❌</center>  |
| GST821                 | <center>✔️</center> | <center>❌</center>  |
| GST122                 | <center>✔️</center> | <center>❌</center>  |
| GST222                 | <center>✔️</center> | <center>❌</center>  |
| GST422                 | <center>✔️</center> | <center>❌</center>  |
| GST822                 | <center>✔️</center> | <center>❌</center>  |
| YUY2                   | <center>✔️</center> | <center>❌</center>  |
| NV12                   | <center>✔️</center> | <center>❌</center>  |
| NV21                   | <center>✔️</center> | <center>❌</center>  |
| UYVY                   | <center>✔️</center> | <center>❌</center>  |
| YUV444P                | <center>✔️</center> | <center>❌</center>  |
| YUV410P                | <center>✔️</center> | <center>❌</center>  |
| YUV420P                | <center>✔️</center> | <center>❌</center>  |
| YUV422P                | <center>✔️</center> | <center>❌</center>  |
| YUV411P                | <center>✔️</center> | <center>❌</center>  |
| UYYVYY411              | <center>✔️</center> | <center>❌</center>  |
| YUV440P                | <center>✔️</center> | <center>❌</center>  |
| YUVA420P               | <center>✔️</center> | <center>❌</center>  |
| AYUV                   | <center>✔️</center> | <center>❌</center>  |
| GRAY8A (LA88)          | <center>✔️</center> | <center>❌</center>  |
| GRAY16                 | <center>✔️</center> | <center>❌</center>  |
| RG88                   | <center>✔️</center> | <center>❌</center>  |
| R8                     | <center>✔️</center> | <center>❌</center>  |
| G8                     | <center>✔️</center> | <center>❌</center>  |
| B8                     | <center>✔️</center> | <center>❌</center>  |
| R16                    | <center>✔️</center> | <center>❌</center>  |
| G16                    | <center>✔️</center> | <center>❌</center>  |
| B16                    | <center>✔️</center> | <center>❌</center>  |
| R32                    | <center>✔️</center> | <center>❌</center>  |
| G32                    | <center>✔️</center> | <center>❌</center>  |
| B32                    | <center>✔️</center> | <center>❌</center>  |
| BUMPMAP_SR             | <center>✔️</center> | <center>❌</center>  |


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

# Image decoding - example

// DXT1 compressed image decoding

```
from reversebox.image.image_decoder import ImageDecoder
from reversebox.image.image_formats import ImageFormats
from reversebox.image.pillow_wrapper import PillowWrapper


def show_img():
    with open("image_data_dxt1_64x64.bin", "rb") as f:
        image_data = f.read()

    img_width: int = 64
    img_height: int = 64
    decoder = ImageDecoder()
    wrapper = PillowWrapper()
    converted_data: bytes = decoder.decode_compressed_image(image_data, img_width, img_height, ImageFormats.BC1_DXT1)
    pil_image = wrapper.get_pillow_image_from_rgba8888_data(converted_data, img_width, img_height)
    pil_image.show()


if __name__ == '__main__':
    show_img()
```


# More Examples

Need more examples? <br>
Check out list of tools written using ReverseBox:
- [Giana's Return ZDA Tool](https://github.com/bartlomiejduda/Tools/blob/master/NEW%20Tools/Gianas%20Return/Gianas_Return_ZDA_Tool.py)
- [ObsCure 2 HVP Extractor](https://github.com/bartlomiejduda/Tools/blob/master/NEW%20Tools/ObsCure%202/ObsCure%202%20HVP%20Tools/Obscure_2_hvp_extractor.py)
- [Tail Concerto Translation Tools](https://github.com/bartlomiejduda/Tools/tree/master/NEW%20Tools/Tail%20Concerto/Tail%20Concerto%20Tools)
- [EA Graphics Manager](https://github.com/bartlomiejduda/EA-Graphics-Manager)
- [Acclaim TRE Tool](https://github.com/bartlomiejduda/Tools/tree/master/NEW%20Tools/Acclaim/Acclaim_TRE_Tool)
- [F-Zero X TEX Tool](https://github.com/bartlomiejduda/Tools/tree/master/NEW%20Tools/F-Zero%20X/TEX%20Tool)
- [ImageHeat](https://github.com/bartlomiejduda/ImageHeat)
- [Hatch Engine Archive Tool](https://github.com/bartlomiejduda/Tools/tree/master/NEW%20Tools/Hatch%20Engine/Hatch%20Engine%20Archive%20Tool)
- [ReverseBox Demo](https://github.com/bartlomiejduda/Tools/tree/master/ReverseBox_Demo)
- [Super Galdelic Hour .egg texture extractor/converter](https://gist.github.com/boringhexi/e3f2e5ad98c39cdafa4913d7db23f81d)
- and more...

# Badges
![PyPI Downloads](https://static.pepy.tech/badge/reversebox)
![PyPI - Downloads](https://img.shields.io/pypi/dm/ReverseBox)
![GitHub License](https://img.shields.io/github/license/bartlomiejduda/ReverseBox)
![GitHub commit activity](https://img.shields.io/github/commit-activity/y/bartlomiejduda/ReverseBox)
![GitHub repo size](https://img.shields.io/github/repo-size/bartlomiejduda/ReverseBox)
![PyPI - Version](https://img.shields.io/pypi/v/ReverseBox)
