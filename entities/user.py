from datetime import datetime

from .abstract import Abstract

class User(Abstract):
    def __init__(self, login: str, password: str, balance: float = 0.0):
        self._login = login
        self._password = password
        self._balance = float(balance)
        self._blocked = False
        self._time_in: datetime | None = None
        self._time_out: datetime | None = None

    @property
    def login(self): return self._login

    @login.setter
    def login(self, login): self._login = login

    @property
    def password(self): return self._password
    
    @password.setter
    def password(self, password): self._password = password

    @property
    def balance(self): return self._balance
    
    @balance.setter
    def balance(self, balance): self._balance = float(balance)

    @property
    def blocked(self): return self._blocked
    
    @blocked.setter
    def blocked(self, blocked): self._blocked = bool(blocked)

    @property
    def time_in(self): return self._time_in
    
    @time_in.setter
    def time_in(self, time_in): self._time_in = time_in

    @property
    def time_out(self): return self._time_out
    
    @time_out.setter
    def time_out(self, time_out): self._time_out = time_out

    def describe(self) -> str:
        role = type(self).__name__

        if self._blocked:
            status = " [заблокирован]"
        else:
            status = ""

        return f"[{role}] {self._login}: {self._balance:.2f} ₽{status}"

    def record(self) -> str:

        if self._time_in:
            tin = self._time_in.strftime("%d.%m.%Y %H:%M:%S") 
        else:
            tin = "-"

        if self._time_out:
            tout = self._time_out.strftime("%d.%m.%Y %H:%M:%S") 
        else:
            tout = "-"

        return f"| {self._login:<10} | {tin:<19} | {tout:<19} |"

    def __eq__(self, other):
        if not isinstance(other, User):
            return NotImplemented
        return self._login == other._login

    def __lt__(self, other):
        return self._balance < other._balance

    def __le__(self, other):
        return self._balance <= other._balance

    def __gt__(self, other):
        return self._balance > other._balance

    def __ge__(self, other):
        return self._balance >= other._balance

    def __hash__(self):
        return hash(self._login)

    def __repr__(self):
        return f"{type(self).__name__}(login={self._login!r}, balance={self._balance})"

    def __str__(self):
        return self.describe()