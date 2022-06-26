import struct

# XOR Cipher used in Retro64 *.ECO files
# Read more here: http://wiki.xentax.com/index.php/Retro64_ECO


def xor_cipher_retro64_eco(input_data: bytes, key: int) -> bytes:
    result: bytes = b''
    for raw_byte in input_data:
        new_key = (201 * key + 11) % 0x7FFF
        key = new_key
        decrypted_byte = raw_byte ^ (new_key % 0xFF)
        result += struct.pack("B", decrypted_byte)

    return result

