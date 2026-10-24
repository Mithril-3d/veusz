"""Test script for Phase 2: Enhanced Metafile (EMF) Clipboard Copy feature."""

import os
import sys
import ctypes
import tempfile
import pyemf3
import importlib.util
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QMimeData

def run_tests():
    print("=== Testing Windows Clipboard EMF Support ===")

    # 1. Test windows_clipboard module directly
    spec = importlib.util.spec_from_file_location(
        'windows_clipboard',
        os.path.join(os.path.dirname(__file__), '..', 'veusz', 'utils', 'windows_clipboard.py')
    )
    wc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(wc)

    # Create temporary EMF file
    with tempfile.NamedTemporaryFile(suffix='.emf', delete=False) as f:
        emf_path = f.name

    try:
        emf = pyemf3.EMF(width=5, height=3, density=300)
        emf.Rectangle(20, 20, 300, 200)
        emf.save(emf_path)

        with open(emf_path, 'rb') as f:
            emf_bytes = f.read()

        # Test QApplication clipboard integration
        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        clipboard = app.clipboard()

        # Step A: Set Qt mime data (PNG)
        mime = QMimeData()
        mime.setData('image/png', b'\x89PNG\r\n\x1a\nfake_png_data')
        clipboard.setMimeData(mime)

        # Step B: Register EMF via windows_clipboard
        success = wc.copy_emf_to_clipboard(emf_bytes)
        assert success is True, "copy_emf_to_clipboard should return True"

        # Step C: Verify clipboard formats
        user32 = ctypes.windll.user32
        CF_ENHMETAFILE = 14
        has_emf = user32.IsClipboardFormatAvailable(CF_ENHMETAFILE)
        assert has_emf, "Clipboard should have CF_ENHMETAFILE (14) available"

        # Also verify that PNG data wasn't destroyed
        mime_out = clipboard.mimeData()
        has_png = mime_out.hasFormat('image/png')
        print(f"Clipboard has CF_ENHMETAFILE: {bool(has_emf)}")
        print(f"Clipboard retained image/png: {has_png}")
        assert has_png, "Qt MIME data should be retained alongside CF_ENHMETAFILE"

        # Step D: Test copy_emf_file_to_clipboard
        success_file = wc.copy_emf_file_to_clipboard(emf_path)
        assert success_file is True, "copy_emf_file_to_clipboard should return True"
        has_emf2 = user32.IsClipboardFormatAvailable(CF_ENHMETAFILE)
        assert has_emf2, "Clipboard should have CF_ENHMETAFILE (14) after file copy"

        print("=== Test 1 (Clipboard API & Hybrid Format): PASS ===")

    finally:
        if os.path.exists(emf_path):
            os.remove(emf_path)

    # 2. Verify treeeditwindow.py modifications
    treeedit_path = os.path.join(
        os.path.dirname(__file__), '..', 'veusz', 'windows', 'treeeditwindow.py'
    )
    with open(treeedit_path, 'r', encoding='utf-8') as f:
        treeedit_content = f.read()

    assert "key='Ctrl+Shift+C'" in treeedit_content, "Shortcut for edit.copy_as_image must be Ctrl+Shift+C"
    assert "windows_clipboard.copy_emf_file_to_clipboard" in treeedit_content, "Must call windows_clipboard.copy_emf_file_to_clipboard"
    assert "export_emf = (sys.platform == 'win32' and document.hasemf)" in treeedit_content, "Must check document.hasemf"
    print("=== Test 2 (treeeditwindow implementation): PASS ===")

    # 3. Verify plotwindow.py modifications
    plotwin_path = os.path.join(
        os.path.dirname(__file__), '..', 'veusz', 'windows', 'plotwindow.py'
    )
    with open(plotwin_path, 'r', encoding='utf-8') as f:
        plotwin_content = f.read()

    assert "'edit.copy_as_image' in self.vzactions" in plotwin_content, "PlotWindow context menu must include edit.copy_as_image"
    print("=== Test 3 (plotwindow context menu): PASS ===")

    print("\nALL PHASE 2 TESTS PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    run_tests()
