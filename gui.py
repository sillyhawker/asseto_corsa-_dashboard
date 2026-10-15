import tkinter as tk
import struct
import ctypes
from collections import deque

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

window = tk.Tk()
window.title("Telemetary")
window.geometry("400x300")
gear_label = tk.Label(
    window,
    font=("Arial", 40)
)

rpms_label = tk.Label(
    window,
    font=("Arial", 20)
)

speed_label = tk.Label(
    window,
    font=("Arial", 20)
)

telemetry_graph = tk.Canvas(
    window,
    width=500,
    height=150
)

gas_line = telemetry_graph.create_line(
    0, 150,
    1, 150,
    width=2
)

gear_label.grid(
    row=0,
    column=0,
    columnspan=2
)

rpms_label.grid(
    row=1,
    column=0,
    padx=20,
    pady=10
)

speed_label.grid(
    row=1,
    column=1
)

telemetry_graph.grid(
    row=2,
    column=0,
    columnspan=2,
    sticky="nsew"
)

window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)

def update_telemetry():
    raw = ctypes.string_at(view, 32)

    gas = struct.unpack("f", raw[4:8])[0]
    brake = struct.unpack("f", raw[8:12])[0]
    gear = struct.unpack("i", raw[16:20])[0] - 1
    rpms = struct.unpack("i", raw[20:24])[0]
    speed_kmh = struct.unpack("f", raw[28:32])[0]

    speed_mph = speed_kmh * 0.621371

    # gas_history.append(gas)
    # brake_history.append(brake)

    # draw_graph()

    if gear == 0:
        gear_label.config(text="N")
    else:
        gear_label.config(text=str(gear))

    rpms_label.config(text=f"{rpms} RPM")
    speed_label.config(text=f"{speed_mph:.1f} mph")

    window.after(50, update_telemetry)

# def draw_graph():

#     width = 500
#     height = 150

#     if len(gas_history) < 2:
#         return

#     points = []

#     for i, gas in enumerate(gas_history):
#         x = i * width / 199
#         y = height - (gas * height)

#         points.extend([x, y])
#     telemetry_graph.coords(gas_line, *points)


# gas_history = deque(maxlen=200)
# brake_history = deque(maxlen=200)

update_telemetry()
window.mainloop()