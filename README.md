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
  - BZIP2 (TODO) ❌
  - GZIP (TODO) ❌
  - JCALG1 (TODO) ❌
  - LZMA (TODO) ❌
  - LZO / LZO1X ✔️ <span style="color:yellow">(wrapper only)</span>
  - LZSS (TODO) ❌
  - MIO0 ✔️
  - NitroSDK (TODO) ❌
  - Oodle (TODO) ❌
  - Refpack (EA Games) ✔️ <span style="color:yellow">(wrapper only)</span>
  - RNC (TODO) ❌
  - ZLIB ✔️ <span style="color:yellow">(wrapper only)</span>
  - (game-specific) Re:Tiyoruga DAT compression ✔️

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
  - Decode RGB121 ✔️
  - Decode RGB121_BYTE ✔️
  - Decode RGBA2222 ✔️
  - Decode RGBX2222 ✔️
  - Decode GRAY8 ✔️
  - Decode ALPHA8 ✔️
  - Decode LA44 ✔️
  - Decode RGBX332 (RGB8) ✔️
  - Decode BGRX332 (BGR8) ✔️
  - Decode/Encode RGB565 ✔️
  - Decode/Encode BGR565 ✔️
  - Decode/Encode RGBX5551 ✔️
  - Decode/Encode RGBT5551 ✔️
  - Decode/Encode RGBA5551 ✔️
  - Decode/Encode BGRA5551 ✔️
  - Decode BGRX5551 ✔️
  - Decode RGBX6666 ✔️
  - Decode RGBA6666 ✔️
  - Decode RGB888 (RGB24) ✔️
  - Decode BGR888 (BGR24) ✔️
  - Decode ARGB4444 ✔️
  - Decode RGBA4444 ✔️
  - Decode ABGR4444 ✔️
  - Decode XBGR4444 ✔️
  - Decode/Encode RGBX4444 ✔️
  - Decode BGRA4444 ✔️
  - Decode BGRX4444 ✔️
  - Decode XRGB1555 ✔️
  - Decode ARGB1555 ✔️
  - Decode ABGR1555 ✔️
  - Decode XBGR1555 ✔️
  - Decode/Encode ARGB8888 ✔️
  - Decode ABGR8888 ✔️
  - Decode/Encode RGBA8888 ✔️
  - Decode/Encode BGRA8888 ✔️
  - Decode RGB48 ✔️
  - Decode BGR48 ✔️
  - Decode/Encode PAL4 ✔️
  - Decode/Encode PAL8 ✔️
  - Decode PAL16 ✔️
  - Decode PAL32 ✔️
  - Decode PAL_I8A8 ✔️
  - Decode N64_RGB5A3 ✔️
  - Decode N64_I4 ✔️
  - Decode N64_I8 ✔️
  - Decode N64_IA4 ✔️
  - Decode N64_IA8 ✔️
  - Decode N64_RGBA32 ✔️
  - Decode N64_CMPR ✔️
  - Decode/Encode BC1/DXT1 ✔️
  - Decode/Encode DXT2 ✔️
  - Decode/Encode BC2/DXT3 ✔️
  - Decode/Encode DXT4 ✔️
  - Decode/Encode BC3/DXT5 ✔️
  - Decode/Encode BC4 ✔️
  - Decode/Encode BC5 ✔️
  - Decode/Encode BC6 ✔️
  - Decode/Encode BC7 ✔️
  - Decode/Encode PVRTCI_2bpp_RGB ✔️
  - Decode/Encode PVRTCI_2bpp_RGBA ✔️
  - Decode/Encode PVRTCI_4bpp_RGB ✔️
  - Decode/Encode PVRTCI_4bpp_RGBA ✔️
  - Decode/Encode PVRTCII_2bpp ✔️
  - Decode/Encode PVRTCII_4bpp ✔️
  - Decode/Encode ETC1 ✔️
  - Decode/Encode BW1bpp ✔️
  - Decode/Encode SharedExponentR9G9B9E5 ✔️
  - Decode/Encode RGBG8888 ✔️
  - Decode/Encode GRGB8888 ✔️
  - Decode/Encode ETC2_RGB ✔️
  - Decode/Encode ETC2_RGBA ✔️
  - Decode/Encode ETC2_RGB_A1 ✔️
  - Decode/Encode EAC_R11 ✔️
  - Decode/Encode EAC_RG11 ✔️
  - Decode/Encode ASTC_4x4 ✔️
  - Decode/Encode ASTC_5x4 ✔️
  - Decode/Encode ASTC_5x5 ✔️
  - Decode/Encode ASTC_6x5 ✔️
  - Decode/Encode ASTC_6x6 ✔️
  - Decode/Encode ASTC_8x5 ✔️
  - Decode/Encode ASTC_8x6 ✔️
  - Decode/Encode ASTC_8x8 ✔️
  - Decode/Encode ASTC_10x5 ✔️
  - Decode/Encode ASTC_10x6 ✔️
  - Decode/Encode ASTC_10x8 ✔️
  - Decode/Encode ASTC_10x10 ✔️
  - Decode/Encode ASTC_12x10 ✔️
  - Decode/Encode ASTC_12x12 ✔️
  - Decode/Encode ASTC_3x3x3 ✔️
  - Decode/Encode ASTC_4x3x3 ✔️
  - Decode/Encode ASTC_4x4x3 ✔️
  - Decode/Encode ASTC_4x4x4 ✔️
  - Decode/Encode ASTC_5x4x4 ✔️
  - Decode/Encode ASTC_5x5x4 ✔️
  - Decode/Encode ASTC_5x5x5 ✔️
  - Decode/Encode ASTC_6x5x5 ✔️
  - Decode/Encode ASTC_6x6x5 ✔️
  - Decode/Encode ASTC_6x6x6 ✔️
  - Decode/Encode BASISU_ETC1S ✔️
  - Decode/Encode BASISU_UASTC ✔️
  - Decode/Encode RGBM ✔️
  - Decode/Encode RGBD ✔️
  - Decode GST121 ✔️
  - Decode GST221 ✔️
  - Decode GST421 ✔️
  - Decode GST821 ✔️
  - Decode GST122 ✔️
  - Decode GST222 ✔️
  - Decode GST422 ✔️
  - Decode GST822 ✔️
  - Decode YUY2 ✔️
  - Decode NV12 ✔️
  - Decode NV21 ✔️
  - Decode UYVY ✔️
  - Decode YUV444P ✔️
  - Decode YUV410P ✔️
  - Decode YUV420P ✔️
  - Decode YUV422P ✔️
  - Decode YUV411P ✔️
  - Decode UYYVYY411 ✔️
  - Decode YUV440P ✔️
  - Decode YUVA420P ✔️
  - Decode AYUV ✔️
  - Decode GRAY8A (LA88) ✔️
  - Decode GRAY16 ✔️
  - Decode RG88 ✔️
  - Decode XRGB8888 ✔️
  - Decode RGBX8888 ✔️
  - Decode XBGR8888 ✔️
  - Decode BGRX8888 ✔️
  - Decode R8 ✔️
  - Decode G8 ✔️
  - Decode B8 ✔️
  - Decode R16 ✔️
  - Decode G16 ✔️
  - Decode B16 ✔️
  - Decode R32 ✔️
  - Decode G32 ✔️
  - Decode B32 ✔️
  - Decode BUMPMAP_SR ✔️
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
  - PS2 GS Texture Compression ✔️
  - RLE TGA compression ✔️
  - PackBits (Macintosh RLE) compression ✔️
  - Executioners RLE compression ✔️
  - Generating mipmaps ✔️

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
