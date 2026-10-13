from PyQt6.QtWidgets import (
    QLabel, QLineEdit, QPushButton, QListWidget, QComboBox,
    QTableWidget, QStatusBar, QCheckBox, QDoubleSpinBox, QGroupBox,
)


class Label(QLabel):
    def __init__(self, text=""):
        super().__init__(text)


class LineEdit(QLineEdit):
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)


class Button(QPushButton):
    def __init__(self, text=""):
        super().__init__(text)


class ListWidget(QListWidget):
    def __init__(self):
        super().__init__()


class ComboBox(QComboBox):
    def __init__(self):
        super().__init__()


class TableWidget(QTableWidget):
    def __init__(self, rows=0, cols=0):
        super().__init__(rows, cols)


class StatusBar(QStatusBar):
    def __init__(self):
        super().__init__()


class CheckBox(QCheckBox):
    def __init__(self, text=""):
        super().__init__(text)


class DoubleSpinBox(QDoubleSpinBox):
    def __init__(self):
        super().__init__()


class GroupBox(QGroupBox):
    def __init__(self, title=""):
        super().__init__(title)