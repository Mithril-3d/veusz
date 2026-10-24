#    Copyright (C) 2026 Veusz developers
#
#    This file is part of Veusz.
#
#    Veusz is free software: you can redistribute it and/or modify it
#    under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.
#
#    Veusz is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#    General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Veusz. If not, see <https://www.gnu.org/licenses/>.
#
##############################################################################

"""Windows clipboard utilities for placing Enhanced Metafile (EMF) data on clipboard."""

import os
import sys
import time
import logging

logger = logging.getLogger(__name__)

CF_ENHMETAFILE = 14

def is_windows():
    """Return True if running on Windows."""
    return sys.platform == 'win32'

def copy_emf_to_clipboard(emf_bytes):
    """Place EMF bytes onto Windows clipboard as CF_ENHMETAFILE.

    Preserves any existing clipboard formats set previously by Qt
    (e.g. image/png or image/svg+xml) so applications that prefer
    vector formats (like MS Office) paste EMF, while bitmap-only
    applications paste PNG.

    Returns True on success, False otherwise.
    """
    if not is_windows():
        return False

    try:
        import ctypes
        user32 = ctypes.windll.user32
        gdi32 = ctypes.windll.gdi32

        # Configure 64-bit ctypes prototypes to avoid pointer truncation
        gdi32.SetEnhMetaFileBits.argtypes = [ctypes.c_uint, ctypes.c_char_p]
        gdi32.SetEnhMetaFileBits.restype = ctypes.c_void_p

        gdi32.DeleteEnhMetaFile.argtypes = [ctypes.c_void_p]
        gdi32.DeleteEnhMetaFile.restype = ctypes.c_bool

        user32.OpenClipboard.argtypes = [ctypes.c_void_p]
        user32.OpenClipboard.restype = ctypes.c_bool

        user32.SetClipboardData.argtypes = [ctypes.c_uint, ctypes.c_void_p]
        user32.SetClipboardData.restype = ctypes.c_void_p

        user32.CloseClipboard.argtypes = []
        user32.CloseClipboard.restype = ctypes.c_bool
    except Exception as e:
        logger.warning('Failed to load Windows DLLs for clipboard: %s', e)
        return False

    # Create HENHMETAFILE from byte array
    hemf = gdi32.SetEnhMetaFileBits(len(emf_bytes), emf_bytes)
    if not hemf:
        logger.warning('SetEnhMetaFileBits failed')
        return False

    # Retry opening clipboard in case another process holds it temporarily
    opened = False
    for _ in range(5):
        if user32.OpenClipboard(None):
            opened = True
            break
        time.sleep(0.05)

    if not opened:
        gdi32.DeleteEnhMetaFile(hemf)
        logger.warning('OpenClipboard failed (clipboard locked)')
        return False

    try:
        res = user32.SetClipboardData(CF_ENHMETAFILE, hemf)
        if not res:
            logger.warning('SetClipboardData(CF_ENHMETAFILE) failed')
            gdi32.DeleteEnhMetaFile(hemf)
            return False
        # Windows now owns hemf handle
        return True
    finally:
        user32.CloseClipboard()

def copy_emf_file_to_clipboard(filepath):
    """Read an EMF file from disk and copy it to the Windows clipboard."""
    if not is_windows() or not os.path.isfile(filepath):
        return False
    with open(filepath, 'rb') as f:
        data = f.read()
    return copy_emf_to_clipboard(data)
