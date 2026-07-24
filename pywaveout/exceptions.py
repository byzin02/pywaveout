# pywaveout/exceptions.py

class PyWaveOutError(Exception):
    pass

class MMSystemError(PyWaveOutError):
    def __init__(self, code, message="MMRESULT error occurred."):
        self.code = code
        self.message = f"{message} (Code: {code})"
        super().__init__(self.message)