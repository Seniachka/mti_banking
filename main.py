import sys
from PyQt6.QtWidgets import QApplication

from entities.bank import Bank
from entities.client import Client
from entities.admin import Admin
from ui.window import MainWindow


def build_bank() -> Bank:
    bank = Bank("ООП-Банк")
    clients = [
        ("Арсений", "1", 1000), ("Иван", "2", 2500), ("Мария", "3", 500),
        ("Артем", "4", 300),   ("София", "5", 7000), ("Гай", "6", 120),
        ("Анна", "7", 999),  ("Генадий", "8", 50),  ("Ирина", "9", 4200),
    ]
    for login, pwd, bal in clients:
        bank.add(Client(login, pwd, bal))
    bank.add(Admin("admin", "admin"))
    return bank


def main():
    app = QApplication(sys.argv)
    window = MainWindow(build_bank())
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()