"""Comprehensive tests for Phase 3: TextFormatToolbar and _EditBox."""

import os
import sys
from PyQt5 import QtWidgets as qt
from PyQt5.QtWidgets import QApplication, QTextEdit, QLineEdit, QWidget
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QKeyEvent

# Setup path and package context
veusz_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if veusz_dir not in sys.path:
    sys.path.insert(0, veusz_dir)

# Mock required module attributes if needed
import types
if 'veusz.qtall' not in sys.modules:
    import PyQt5.QtWidgets
    import PyQt5.QtGui
    import PyQt5.QtCore
    m = types.ModuleType('veusz.qtall')
    m.__dict__.update(PyQt5.QtWidgets.__dict__)
    m.__dict__.update(PyQt5.QtGui.__dict__)
    m.__dict__.update(PyQt5.QtCore.__dict__)
    sys.modules['veusz.qtall'] = m

if 'veusz.setting.settingdb' not in sys.modules:
    s_mod = types.ModuleType('veusz.setting.settingdb')
    class MockSettingDB(dict):
        def color(self, name):
            from PyQt5.QtGui import QColor
            return QColor('red')
    s_mod.settingdb = MockSettingDB()
    sys.modules['veusz.setting.settingdb'] = s_mod

if 'veusz.utils' not in sys.modules:
    u_mod = types.ModuleType('veusz.utils')
    u_mod.positionFloatingPopup = lambda widget, parent: None
    class InvalidType(Exception): pass
    u_mod.InvalidType = InvalidType
    sys.modules['veusz.utils'] = u_mod

# Now import controls
import importlib.util
spec = importlib.util.spec_from_file_location(
    'veusz.setting.controls',
    os.path.join(veusz_dir, 'veusz', 'setting', 'controls.py')
)
controls = importlib.util.module_from_spec(spec)
sys.modules['veusz.setting.controls'] = controls
spec.loader.exec_module(controls)

def run_tests():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    print("=== Testing TextFormatToolbar ===")
    te = QTextEdit()
    toolbar = controls.TextFormatToolbar(textwidget=te)

    # 1. Test bold with selection
    te.setPlainText("Hello World")
    cursor = te.textCursor()
    cursor.setPosition(6)
    cursor.setPosition(11, cursor.KeepAnchor)
    te.setTextCursor(cursor)

    toolbar.wrapSelection(r"\bold{", "}")
    assert te.toPlainText() == "Hello \\bold{World}", f"Got: {te.toPlainText()}"
    print("Toolbar wrap selection (bold): PASS")

    # 2. Test italic without selection
    te.setPlainText("Test ")
    cursor = te.textCursor()
    cursor.setPosition(5)
    te.setTextCursor(cursor)

    toolbar.wrapSelection(r"\italic{", "}")
    assert te.toPlainText() == "Test \\italic{}"
    assert te.textCursor().position() == 13 # inside {}
    print("Toolbar insert without selection: PASS")

    # 3. Test insert Greek character
    toolbar.insertText(r"\alpha")
    assert te.toPlainText() == "Test \\italic{\\alpha}"
    print("Toolbar insert Greek char: PASS")

    # 4. Test insert math symbol
    toolbar.insertText(r"\pm")
    assert te.toPlainText() == "Test \\italic{\\alpha\\pm}"
    print("Toolbar insert math symbol: PASS")

    # 5. Test with QLineEdit
    le = QLineEdit()
    toolbar.setTextWidget(le)
    le.setText("x + y = 0")
    le.setSelection(0, 1) # select 'x'
    toolbar.wrapSelection(r"\italic{", "}")
    assert le.text() == "\\italic{x} + y = 0", f"Got: {le.text()}"
    print("Toolbar with QLineEdit: PASS")

    # 6. Test _EditBox instantiation and structure
    parent = QWidget()
    box = controls._EditBox("sample text", False, parent)
    assert hasattr(box, 'toolbar'), "_EditBox must have a toolbar"
    assert hasattr(box, 'textedit'), "_EditBox must have a textedit"
    assert box.textedit.toPlainText() == "sample text"
    print("_EditBox structure: PASS")

    # 7. Test _EditBox shortcuts
    box.textedit.selectAll()
    key_event = QKeyEvent(
        QEvent.Type.KeyPress,
        Qt.Key.Key_B,
        Qt.KeyboardModifier.ControlModifier
    )
    res = box.eventFilter(box.textedit, key_event)
    assert res is True, "Ctrl+B should be handled by eventFilter"
    assert box.textedit.toPlainText() == "\\bold{sample text}"
    print("_EditBox Ctrl+B shortcut: PASS")

    # 8. Test _EditBox Escape key
    key_esc = QKeyEvent(
        QEvent.Type.KeyPress,
        Qt.Key.Key_Escape,
        Qt.KeyboardModifier.NoModifier
    )
    box.eventFilter(box.textedit, key_esc)
    assert box.textedit.toPlainText() == "sample text", "Escape must restore original text"
    print("_EditBox Escape restore: PASS")

    box.close()

    print("\nALL PHASE 3 FORMATTING TESTS PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    run_tests()
