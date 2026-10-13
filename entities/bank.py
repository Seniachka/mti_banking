from .abstract import Abstract
from .mapping import Mapping
from .user import User


class Bank(Abstract):
    def __init__(self, name: str):
        self._name = name
        self._users = Mapping()

    @property
    def name(self): return self._name
    
    @name.setter
    def name(self, name): self._name = name

    def add(self, user: User):
        self._users.put(user.login, user)

    def find(self, login: str) -> User | None:
        return self._users.get(login)

    def all(self) -> list[User]:
        return [user for _, user in self._users.items()]

    def authenticate(self, login: str, password: str) -> User:
        user = self.find(login)

        if user is None or user.password != password:
            raise ValueError("Неверный логин или пароль")
        
        if user.blocked:
            raise ValueError("Аккаунт заблокирован")
        
        return user

    def describe(self) -> str:
        return f"Банк «{self._name}», пользователей: {len(self)}"

    def record(self) -> str:
        lines = [self.describe()]
        for user in self.all():
            lines.append("  " + user.record())
        return "\n".join(lines)

    @staticmethod
    def save_report(path: str, users: list[User]):
        border = "+------------+---------------------+---------------------+"
        with open(path, "w", encoding="utf-8") as f:
            f.write(border + "\n")
            f.write("| login      | time_in             | time_out            |\n")
            f.write(border + "\n")
            for user in users:
                f.write(user.record() + "\n")
            f.write(border + "\n")

    def __eq__(self, other):
        if not isinstance(other, Bank):
            return NotImplemented
        return self._name == other._name

    def __len__(self):
        return len(self._users)

    def __repr__(self):
        return f"Bank({self._name!r}, users={len(self)})"

    def __str__(self):
        return self._name