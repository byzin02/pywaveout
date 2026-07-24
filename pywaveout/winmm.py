import ctypes

try:
    winmm_dll = ctypes.WinDLL("winmm")
except OSError:
    winmm_dll = None