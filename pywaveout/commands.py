import ctypes
from ctypes import wintypes

from .winmm import winmm_dll
from .structures import (
    HWAVEOUT,
    LPHWAVEOUT,
    WAVEFORMATEX,
    _WAVEFORMATEX,
    WAVEHDR,
    _WAVEHDR,
    WAVEOUTCAPSW,
    _WAVEOUTCAPSW,
    MMTIME,
    _MMTIME,
    MMRESULT,
    DWORD_PTR,
)

def _handle_arg(hwo):
    if isinstance(hwo, HWAVEOUT):
        return hwo.value
    return hwo

def _struct_arg(obj):
    if hasattr(obj, "_struct"):
        return obj._struct
    return obj

def _struct_ptr(obj):
    if hasattr(obj, "_struct"):
        return ctypes.byref(obj._struct)
    return obj

def _normalize_size(cb, struct_type):
    if cb is None or cb is struct_type:
        return ctypes.sizeof(struct_type)
    return cb

if winmm_dll:
    # waveOutGetNumDevs
    _waveOutGetNumDevs = winmm_dll.waveOutGetNumDevs
    _waveOutGetNumDevs.argtypes = []
    _waveOutGetNumDevs.restype = ctypes.c_uint

    def waveOutGetNumDevs() -> int:
        return _waveOutGetNumDevs()

    # waveOutGetDevCaps
    _waveOutGetDevCapsW = winmm_dll.waveOutGetDevCapsW
    _waveOutGetDevCapsW.argtypes = [
        ctypes.c_void_p,
        ctypes.POINTER(_WAVEOUTCAPSW),
        ctypes.c_uint,
    ]
    _waveOutGetDevCapsW.restype = MMRESULT

    def waveOutGetDevCaps(uDeviceID, pwoc=None, cbwoc=None):
        if pwoc is None:
            pwoc = WAVEOUTCAPSW()
            cbwoc = _normalize_size(cbwoc, _WAVEOUTCAPSW)
            rr = _waveOutGetDevCapsW(uDeviceID, ctypes.byref(pwoc._struct), cbwoc)
            return rr, pwoc

        cbwoc = _normalize_size(cbwoc, _WAVEOUTCAPSW)
        return _waveOutGetDevCapsW(uDeviceID, _struct_ptr(pwoc), cbwoc)

    # waveOutOpen
    _waveOutOpen = winmm_dll.waveOutOpen
    _waveOutOpen.argtypes = [
        LPHWAVEOUT,
        wintypes.UINT,
        ctypes.POINTER(_WAVEFORMATEX),
        DWORD_PTR,
        DWORD_PTR,
        wintypes.DWORD,
    ]
    _waveOutOpen.restype = MMRESULT

    def waveOutOpen(phwo, uDeviceID, pwfx, dwCallback, dwInstance, fdwOpen):
        pwfx = _struct_ptr(pwfx)

        if isinstance(phwo, HWAVEOUT):
            tmp = wintypes.HANDLE()
            rr = _waveOutOpen(
                ctypes.byref(tmp),
                uDeviceID,
                pwfx,
                dwCallback,
                dwInstance,
                fdwOpen,
            )
            phwo.value = wintypes.HANDLE(tmp.value)
            return rr

        return _waveOutOpen(phwo, uDeviceID, pwfx, dwCallback, dwInstance, fdwOpen)

    # waveOutClose
    _waveOutClose = winmm_dll.waveOutClose
    _waveOutClose.argtypes = [wintypes.HANDLE]
    _waveOutClose.restype = MMRESULT

    def waveOutClose(hwo) -> int:
        return _waveOutClose(_handle_arg(hwo))

    # waveOutPrepareHeader
    _waveOutPrepareHeader = winmm_dll.waveOutPrepareHeader
    _waveOutPrepareHeader.argtypes = [wintypes.HANDLE, ctypes.POINTER(_WAVEHDR), wintypes.UINT]
    _waveOutPrepareHeader.restype = MMRESULT

    def waveOutPrepareHeader(hwo, pwh, cbwh=None):
        cbwh = _normalize_size(cbwh, _WAVEHDR)
        return _waveOutPrepareHeader(_handle_arg(hwo), _struct_ptr(pwh), cbwh)

    # waveOutUnprepareHeader
    _waveOutUnprepareHeader = winmm_dll.waveOutUnprepareHeader
    _waveOutUnprepareHeader.argtypes = [wintypes.HANDLE, ctypes.POINTER(_WAVEHDR), wintypes.UINT]
    _waveOutUnprepareHeader.restype = MMRESULT

    def waveOutUnprepareHeader(hwo, pwh, cbwh=None):
        cbwh = _normalize_size(cbwh, _WAVEHDR)
        return _waveOutUnprepareHeader(_handle_arg(hwo), _struct_ptr(pwh), cbwh)

    # waveOutWrite
    _waveOutWrite = winmm_dll.waveOutWrite
    _waveOutWrite.argtypes = [wintypes.HANDLE, ctypes.POINTER(_WAVEHDR), wintypes.UINT]
    _waveOutWrite.restype = MMRESULT

    def waveOutWrite(hwo, pwh, cbwh=None):
        cbwh = _normalize_size(cbwh, _WAVEHDR)
        return _waveOutWrite(_handle_arg(hwo), _struct_ptr(pwh), cbwh)

    # waveOutPause
    _waveOutPause = winmm_dll.waveOutPause
    _waveOutPause.argtypes = [wintypes.HANDLE]
    _waveOutPause.restype = MMRESULT

    def waveOutPause(hwo: HWAVEOUT) -> int:
        return _waveOutPause(_handle_arg(hwo))

    # waveOutRestart
    _waveOutRestart = winmm_dll.waveOutRestart
    _waveOutRestart.argtypes = [wintypes.HANDLE]
    _waveOutRestart.restype = MMRESULT

    def waveOutRestart(hwo: HWAVEOUT) -> int:
        return _waveOutRestart(_handle_arg(hwo))

    # waveOutReset
    _waveOutReset = winmm_dll.waveOutReset
    _waveOutReset.argtypes = [wintypes.HANDLE]
    _waveOutReset.restype = MMRESULT

    def waveOutReset(hwo: HWAVEOUT) -> int:
        return _waveOutReset(_handle_arg(hwo))

    # waveOutBreakLoop
    _waveOutBreakLoop = winmm_dll.waveOutBreakLoop
    _waveOutBreakLoop.argtypes = [wintypes.HANDLE]
    _waveOutBreakLoop.restype = MMRESULT

    def waveOutBreakLoop(hwo: HWAVEOUT) -> int:
        return _waveOutBreakLoop(_handle_arg(hwo))

    # waveOutGetPosition
    _waveOutGetPosition = winmm_dll.waveOutGetPosition
    _waveOutGetPosition.argtypes = [wintypes.HANDLE, ctypes.POINTER(_MMTIME), wintypes.UINT]
    _waveOutGetPosition.restype = MMRESULT

    def waveOutGetPosition(hwo, pmmt=None, cbmmt=None):
        if pmmt is None:
            pmmt = MMTIME()
            pmmt.wType = 1  # TIME_MS
            cbmmt = _normalize_size(cbmmt, _MMTIME)
            rr = _waveOutGetPosition(_handle_arg(hwo), ctypes.byref(pmmt._struct), cbmmt)
            return rr, pmmt

        cbmmt = _normalize_size(cbmmt, _MMTIME)
        return _waveOutGetPosition(_handle_arg(hwo), _struct_ptr(pmmt), cbmmt)

    # waveOutGetVolume
    _waveOutGetVolume = winmm_dll.waveOutGetVolume
    _waveOutGetVolume.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
    _waveOutGetVolume.restype = MMRESULT

    def waveOutGetVolume(hwo, pdwVolume=None):
        if pdwVolume is None:
            vol = wintypes.DWORD()
            rr = _waveOutGetVolume(_handle_arg(hwo), ctypes.byref(vol))
            return rr, vol.value
        return _waveOutGetVolume(_handle_arg(hwo), pdwVolume)

    # waveOutSetVolume
    _waveOutSetVolume = winmm_dll.waveOutSetVolume
    _waveOutSetVolume.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    _waveOutSetVolume.restype = MMRESULT

    def waveOutSetVolume(hwo: HWAVEOUT, dwVolume: int) -> int:
        return _waveOutSetVolume(_handle_arg(hwo), dwVolume)

    # waveOutGetPitch
    _waveOutGetPitch = winmm_dll.waveOutGetPitch
    _waveOutGetPitch.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
    _waveOutGetPitch.restype = MMRESULT

    def waveOutGetPitch(hwo, pdwPitch=None):
        if pdwPitch is None:
            pitch = wintypes.DWORD()
            rr = _waveOutGetPitch(_handle_arg(hwo), ctypes.byref(pitch))
            return rr, pitch.value
        return _waveOutGetPitch(_handle_arg(hwo), pdwPitch)

    # waveOutSetPitch
    _waveOutSetPitch = winmm_dll.waveOutSetPitch
    _waveOutSetPitch.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    _waveOutSetPitch.restype = MMRESULT

    def waveOutSetPitch(hwo: HWAVEOUT, dwPitch: int) -> int:
        return _waveOutSetPitch(_handle_arg(hwo), dwPitch)

    # waveOutGetPlaybackRate
    _waveOutGetPlaybackRate = winmm_dll.waveOutGetPlaybackRate
    _waveOutGetPlaybackRate.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
    _waveOutGetPlaybackRate.restype = MMRESULT

    def waveOutGetPlaybackRate(hwo, pdwRate=None):
        if pdwRate is None:
            rate = wintypes.DWORD()
            rr = _waveOutGetPlaybackRate(_handle_arg(hwo), ctypes.byref(rate))
            return rr, rate.value
        return _waveOutGetPlaybackRate(_handle_arg(hwo), pdwRate)

    # waveOutSetPlaybackRate
    _waveOutSetPlaybackRate = winmm_dll.waveOutSetPlaybackRate
    _waveOutSetPlaybackRate.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    _waveOutSetPlaybackRate.restype = MMRESULT

    def waveOutSetPlaybackRate(hwo: HWAVEOUT, dwRate: int) -> int:
        return _waveOutSetPlaybackRate(_handle_arg(hwo), dwRate)

    # waveOutGetID
    _waveOutGetID = winmm_dll.waveOutGetID
    _waveOutGetID.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.UINT)]
    _waveOutGetID.restype = MMRESULT

    def waveOutGetID(hwo, puDeviceID=None):
        if puDeviceID is None:
            dev_id = wintypes.UINT()
            rr = _waveOutGetID(_handle_arg(hwo), ctypes.byref(dev_id))
            return rr, dev_id.value
        return _waveOutGetID(_handle_arg(hwo), puDeviceID)

    # waveOutGetErrorText
    _waveOutGetErrorTextW = winmm_dll.waveOutGetErrorTextW
    _waveOutGetErrorTextW.argtypes = [MMRESULT, ctypes.c_void_p, wintypes.UINT]
    _waveOutGetErrorTextW.restype = MMRESULT

    def waveOutGetErrorText(mmrError: int, pszText=None, cchText: int = 512):
        if pszText is None:
            buf = ctypes.create_unicode_buffer(cchText)
            rr = _waveOutGetErrorTextW(mmrError, ctypes.cast(buf, ctypes.c_void_p), cchText)
            return rr, buf.value
        return _waveOutGetErrorTextW(mmrError, pszText, cchText)

    # waveOutMessage
    _waveOutMessage = winmm_dll.waveOutMessage
    _waveOutMessage.argtypes = [wintypes.HANDLE, wintypes.UINT, DWORD_PTR, DWORD_PTR]
    _waveOutMessage.restype = MMRESULT

    def waveOutMessage(hwo: HWAVEOUT, uMsg: int, dw1: int, dw2: int) -> int:
        return _waveOutMessage(_handle_arg(hwo), uMsg, dw1, dw2)