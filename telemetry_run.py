import ctypes
import struct
import time
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

OpenFileMapping = kernel32.OpenFileMappingW

OpenFileMapping.argtypes = [
    ctypes.c_uint32,
    ctypes.c_bool,
    ctypes.c_wchar_p
]

OpenFileMapping.restype = ctypes.c_void_p

MapViewOfFile = kernel32.MapViewOfFile

MapViewOfFile.argtypes = [
    ctypes.c_void_p,
    ctypes.c_uint32,
    ctypes.c_uint32,
    ctypes.c_uint32,
    ctypes.c_size_t
]

MapViewOfFile.restype = ctypes.c_void_p


FILE_MAP_READ = 0x0004

handle = OpenFileMapping(
    FILE_MAP_READ,
    False,
    "Local\\acpmf_physics"
)
view = MapViewOfFile(
    handle,
    FILE_MAP_READ,
    0,
    0,
    32
)

if view:
    print("Memory mapped!")
    print("Address:", hex(view))
else:
    print("Mapping failed:", ctypes.get_last_error())

while True:
    raw = ctypes.string_at(view, 32)
    #print(raw)

    packet_id = struct.unpack("i", raw[0:4])[0]


    gas = struct.unpack("f", raw[4:8])[0]

    brake = struct.unpack("f", raw[8:12])[0]


    fuel = struct.unpack("f", raw[12:16])


    gear = struct.unpack("i", raw[16:20])[0] -1


    rpms = struct.unpack("f", raw[20:24])[0]


    steer_angle = struct.unpack("f", raw[24:28])


    speed = struct.unpack("f", raw[28:32])[0] * 0.621371

    if gear == 0:
        gear = 'N'

    print(
    f"Speed: {speed:.1f} mph | "
    f"RPM: {rpms*1E45:.0f} | "
    f"Gear: {gear} | "
    f"Gas: {gas:.2f} | "
    f"Brake: {brake:.2f}"
    )
