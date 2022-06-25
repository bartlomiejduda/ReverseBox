# Info

ReverseBox is a Python library with a set of functions
useful in reverse engineering.


# Examples

Here is example usage:


// Checksum calculation
```
from reversebox.checksum import checksum_crc16
from reversebox.common import common


test_data = b'123456789'
crc16_handler = checksum_crc16.CRC16Handler()
crc16 = crc16_handler.calculate_crc16(test_data)
print("CRC16_INT: ", crc16)
print("CRC16_STR: ", common.convert_int_to_hex_string(crc16))
```
// Output
```
CRC16_INT:  47933
CRC16_STR:  0xBB3D
```