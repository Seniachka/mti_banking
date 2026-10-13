from datetime import datetime

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QFormLayout, QLineEdit,
    QTableWidgetItem, QMessageBox, QHeaderView,
)

from entities.bank import Bank
from entities.client import Client
from entities.admin import Admin
from entities.user import User

from .components import (
    Label, LineEdit, Button, ListWidget, ComboBox,
    TableWidget, StatusBar, CheckBox, DoubleSpinBox, GroupBox,
)


class MainWindow(QMainWindow):
    def __init__(self, bank: Bank):
        super().__init__()
        self._bank = bank
        self._current: User | None = None

        self.setWindowTitle(bank.name)
        self.resize(760, 720)
        self._build_ui()
        self._apply_style()
        self._refresh_all()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(10)

        self.login_box = GroupBox("Вход")
        form = QFormLayout(self.login_box)

        self.login_input = LineEdit("Логин")
        form.addRow(Label("Логин:"), self.login_input)

        self.password_input = LineEdit("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form.addRow(Label("Пароль:"), self.password_input)

        self.show_pass = CheckBox("Показать пароль")
        self.show_pass.toggled.connect(self._toggle_pass)
        form.addRow(Label(""), self.show_pass)

        self.login_btn = Button("Войти")
        self.login_btn.clicked.connect(self._do_login)
        form.addRow(Label(""), self.login_btn)

        self.logout_btn = Button("Выйти")
        self.logout_btn.clicked.connect(self._do_logout)
        self.logout_btn.setEnabled(False)
        form.addRow(Label(""), self.logout_btn)

        root.addWidget(self.login_box)

        self.users_box = GroupBox("Пользователи (двойной клик — подставить логин)")
        v = QVBoxLayout(self.users_box)
        self.users_list = ListWidget()
        self.users_list.itemDoubleClicked.connect(self._pick_user)
        v.addWidget(self.users_list)
        root.addWidget(self.users_box)

        self.client_box = GroupBox("Операции клиента")
        fc = QFormLayout(self.client_box)

        self.client_info = Label("—")
        fc.addRow(Label("Счёт:"), self.client_info)

        self.op_type = ComboBox()
        self.op_type.addItems(["Пополнение", "Снятие"])
        fc.addRow(Label("Операция:"), self.op_type)

        self.op_amount = DoubleSpinBox()
        self.op_amount.setRange(0.01, 1_000_000)
        self.op_amount.setValue(100)
        self.op_amount.setSuffix(" ₽")
        fc.addRow(Label("Сумма:"), self.op_amount)

        self.exec_btn = Button("Выполнить")
        self.exec_btn.clicked.connect(self._do_client_op)
        fc.addRow(Label(""), self.exec_btn)

        self.client_box.setVisible(False)
        root.addWidget(self.client_box)

        self.admin_box = GroupBox("Управление пользователями (только админ)")
        fa = QFormLayout(self.admin_box)

        self.admin_combo = ComboBox()
        fa.addRow(Label("Пользователь:"), self.admin_combo)

        self.ban_btn = Button("Забанить")
        self.ban_btn.clicked.connect(self._do_ban)
        fa.addRow(Label(""), self.ban_btn)

        self.unban_btn = Button("Разбанить")
        self.unban_btn.clicked.connect(self._do_unban)
        fa.addRow(Label(""), self.unban_btn)

        self.admin_box.setVisible(False)
        root.addWidget(self.admin_box)

        self.table = TableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Логин", "Баланс", "Статус"])
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        root.addWidget(self.table)

        self.setStatusBar(StatusBar())
        self.statusBar().showMessage("Готово")

    def _apply_style(self):
        self.setStyleSheet("""
            QWidget { font-family: 'Segoe UI', Arial; font-size: 11pt; }
            QGroupBox {
                border: 1px solid #cfcfcf;
                border-radius: 8px;
                margin-top: 10px;
                padding: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin; left: 12px; padding: 0 4px;
            }
            QPushButton {
                background: #2d6cdf; color: white;
                border-radius: 6px; padding: 6px 16px; font-weight: 600;
            }
            QPushButton:hover { background: #1f57b8; }
            QPushButton:disabled { background: #aaa; }
            QLineEdit, QComboBox, QDoubleSpinBox {
                border: 1px solid #bbb; border-radius: 6px; padding: 5px;
            }
        """)

    def _refresh_all(self):
        self._refresh_users_list()
        self._refresh_admin_combo()
        self._refresh_table()

    def _refresh_users_list(self):
        self.users_list.clear()
        for user in self._bank.all():
            self.users_list.addItem(f"{user.login} / {user.password}  —  {user.describe()}")

    def _refresh_admin_combo(self):
        self.admin_combo.clear()
        for user in self._bank.all():
            if user is self._current:
                continue  # себя банить нельзя
            self.admin_combo.addItem(user.login)

    def _refresh_table(self):
        self.table.setRowCount(0)
        for user in self._bank.all():
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(user.login))
            self.table.setItem(row, 1, QTableWidgetItem(f"{user.balance:.2f} ₽"))
            self.table.setItem(
                row, 2,
                QTableWidgetItem("заблокирован" if user.blocked else "активен")
            )

    def _update_role_panels(self):
        is_client = isinstance(self._current, Client)
        is_admin = isinstance(self._current, Admin)
        self.client_box.setVisible(is_client)
        self.admin_box.setVisible(is_admin)
        if is_client:
            self.client_info.setText(self._current.describe())

    def _toggle_pass(self, checked: bool):
        self.password_input.setEchoMode(
            QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password
        )

    def _pick_user(self, item):
        try:
            login = item.text().split(" / ")[0]
            pwd = item.text().split(" / ")[1].split("  —  ")[0]
        except IndexError:
            return
        self.login_input.setText(login)
        self.password_input.setText(pwd)

    def _do_login(self):
        login = self.login_input.text().strip()
        password = self.password_input.text()
        try:
            user = self._bank.authenticate(login, password)
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка входа", str(e))
            return

        user.time_in = datetime.now()
        user.time_out = None
        self._current = user

        self.login_input.setEnabled(False)
        self.password_input.setEnabled(False)
        self.login_btn.setEnabled(False)
        self.logout_btn.setEnabled(True)

        self._update_role_panels()
        self._refresh_admin_combo()
        self._refresh_table()
        self.statusBar().showMessage(f"Вы вошли как {user.login}")

    def _do_logout(self):
        if self._current is not None:
            self._current.time_out = datetime.now()
        self._current = None

        self.login_input.setEnabled(True)
        self.password_input.setEnabled(True)
        self.login_btn.setEnabled(True)
        self.logout_btn.setEnabled(False)

        self.client_box.setVisible(False)
        self.admin_box.setVisible(False)

        self._refresh_all()
        self.statusBar().showMessage("Вы вышли из аккаунта")

    def _do_client_op(self):
        if not isinstance(self._current, Client):
            return
        amount = self.op_amount.value()
        try:
            if self.op_type.currentText() == "Пополнение":
                self._current.deposit(amount)
            else:
                self._current.withdraw(amount)
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка операции", str(e))
            return

        self.client_info.setText(self._current.describe())
        self._refresh_users_list()
        self._refresh_table()
        self.statusBar().showMessage(
            f"{self.op_type.currentText()} на {amount:.2f} ₽")

    def _do_ban(self):
        if not isinstance(self._current, Admin):
            return
        login = self.admin_combo.currentText()
        target = self._bank.find(login)
        if target is None:
            return
        self._current.ban(target)
        self._refresh_all()
        self.statusBar().showMessage(f"{login} забанен")

    def _do_unban(self):
        if not isinstance(self._current, Admin):
            return
        login = self.admin_combo.currentText()
        target = self._bank.find(login)
        if target is None:
            return
        self._current.unban(target)
        self._refresh_all()
        self.statusBar().showMessage(f"{login} разбанен")

    def closeEvent(self, event):
        if self._current is not None:
            self._current.time_out = datetime.now()
        try:
            Bank.save_report("report.txt", self._bank.all())
        except OSError as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить отчёт: {e}")
        event.accept()