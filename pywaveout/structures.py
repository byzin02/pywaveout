import ctypes
from ctypes import wintypes

MMRESULT = wintypes.UINT
DWORD_PTR = (
    ctypes.c_ulonglong if ctypes.sizeof(ctypes.c_void_p) == 8 else ctypes.c_ulong
)

HWAVEOUT_HANDLE = wintypes.HANDLE
LPHWAVEOUT = ctypes.POINTER(HWAVEOUT_HANDLE)


class _WAVEFORMATEX(ctypes.Structure):
    _fields_ = [
        ("wFormatTag", wintypes.WORD),
        ("nChannels", wintypes.WORD),
        ("nSamplesPerSec", wintypes.DWORD),
        ("nAvgBytesPerSec", wintypes.DWORD),
        ("nBlockAlign", wintypes.WORD),
        ("wBitsPerSample", wintypes.WORD),
        ("cbSize", wintypes.WORD),
    ]


class WAVEFORMATEX:
    __slots__ = ("_struct",)

    wFormatTag: wintypes.WORD
    nChannels: wintypes.WORD
    nSamplesPerSec: wintypes.DWORD
    nAvgBytesPerSec: wintypes.DWORD
    nBlockAlign: wintypes.WORD
    wBitsPerSample: wintypes.WORD
    cbSize: wintypes.WORD

    def __init__(
        self,
        wFormatTag=0,
        nChannels=0,
        nSamplesPerSec=0,
        nAvgBytesPerSec=0,
        nBlockAlign=0,
        wBitsPerSample=0,
        cbSize=0,
    ):
        object.__setattr__(
            self,
            "_struct",
            _WAVEFORMATEX(
                wFormatTag,
                nChannels,
                nSamplesPerSec,
                nAvgBytesPerSec,
                nBlockAlign,
                wBitsPerSample,
                cbSize,
            ),
        )

    def __getattr__(self, name):
        return getattr(self._struct, name)

    def __setattr__(self, name, value):
        if name == "_struct":
            object.__setattr__(self, name, value)
            return
        setattr(self._struct, name, value)


class _WAVEHDR(ctypes.Structure):
    _fields_ = [
        ("lpData", ctypes.c_void_p),
        ("dwBufferLength", wintypes.DWORD),
        ("dwBytesRecorded", wintypes.DWORD),
        ("dwUser", DWORD_PTR),
        ("dwFlags", wintypes.DWORD),
        ("dwLoops", wintypes.DWORD),
        ("lpNext", ctypes.c_void_p),
        ("reserved", DWORD_PTR),
    ]


class WAVEHDR:
    __slots__ = (
        "_struct",
        "_buffer",
        "_c_buffer",
    )

    lpData: bytes | bytearray | memoryview
    dwBufferLength: wintypes.DWORD
    dwBytesRecorded: wintypes.DWORD
    dwUser: DWORD_PTR
    dwFlags: wintypes.DWORD
    dwLoops: wintypes.DWORD
    lpNext: ctypes.c_void_p
    reserved: DWORD_PTR

    def __init__(self):
        object.__setattr__(self, "_struct", _WAVEHDR())
        object.__setattr__(self, "_buffer", None)
        object.__setattr__(self, "_c_buffer", None)

    @property
    def lpData(self):
        return self._buffer

    @lpData.setter
    def lpData(self, value):
        if isinstance(value, bytes):
            value = bytearray(value)
        elif isinstance(value, memoryview):
            if value.readonly or not value.contiguous:
                value = bytearray(value.tobytes())

        if value is None:
            object.__setattr__(self, "_buffer", None)
            object.__setattr__(self, "_c_buffer", None)
            self._struct.lpData = None
            return

        object.__setattr__(self, "_buffer", value)

        c_buffer = (ctypes.c_byte * len(value)).from_buffer(value)
        object.__setattr__(self, "_c_buffer", c_buffer)

        self._struct.lpData = ctypes.cast(c_buffer, ctypes.c_void_p)

    def __getattr__(self, name):
        return getattr(self._struct, name)

    def __setattr__(self, name, value):
        if name == "lpData":
            type(self).lpData.fset(self, value)
            return

        if name in ("_struct", "_buffer", "_c_buffer"):
            object.__setattr__(self, name, value)
            return

        setattr(self._struct, name, value)


class _WAVEOUTCAPSW(ctypes.Structure):
    _fields_ = [
        ("wMid", wintypes.WORD),
        ("wPid", wintypes.WORD),
        ("vDriverVersion", wintypes.DWORD),
        ("szPname", wintypes.WCHAR * 32),
        ("dwFormats", wintypes.DWORD),
        ("wChannels", wintypes.WORD),
        ("wReserved1", wintypes.WORD),
        ("dwSupport", wintypes.DWORD),
    ]


class WAVEOUTCAPSW:
    __slots__ = ("_struct",)

    wMid: wintypes.WORD
    wPid: wintypes.WORD
    vDriverVersion: wintypes.DWORD
    szPname: str
    dwFormats: wintypes.DWORD
    wChannels: wintypes.WORD
    wReserved1: wintypes.WORD
    dwSupport: wintypes.DWORD

    def __init__(self):
        object.__setattr__(self, "_struct", _WAVEOUTCAPSW())

    def __getattr__(self, name):
        return getattr(self._struct, name)

    def __setattr__(self, name, value):
        if name == "_struct":
            object.__setattr__(self, name, value)
            return
        setattr(self._struct, name, value)


WAVEOUTCAPS = WAVEOUTCAPSW


class _MMTIME_UNION(ctypes.Union):
    _fields_ = [
        ("ms", wintypes.DWORD),
        ("samples", wintypes.DWORD),
        ("cb", wintypes.DWORD),
        ("ticks", wintypes.DWORD),
    ]


class _MMTIME(ctypes.Structure):
    _fields_ = [
        ("wType", wintypes.UINT),
        ("u", _MMTIME_UNION),
    ]


class MMTIME:
    __slots__ = ("_struct",)

    wType: wintypes.UINT
    u: _MMTIME_UNION

    def __init__(self):
        object.__setattr__(self, "_struct", _MMTIME())

    def __getattr__(self, name):
        return getattr(self._struct, name)

    def __setattr__(self, name, value):
        if name == "_struct":
            object.__setattr__(self, name, value)
            return
        setattr(self._struct, name, value)


class HWAVEOUT:
    __slots__ = ("value",)

    value: HWAVEOUT_HANDLE

    def __init__(self, value=0):
        if isinstance(value, HWAVEOUT_HANDLE):
            handle = value
        else:
            handle = HWAVEOUT_HANDLE(value)
        object.__setattr__(self, "value", handle)

    def __int__(self):
        return int(self.value.value or 0)

    def __bool__(self):
        return bool(int(self))

    def __repr__(self):
        return f"HWAVEOUT({self.value.value})"