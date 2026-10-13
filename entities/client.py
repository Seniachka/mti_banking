from .user import User


class Client(User):
    def deposit(self, amount: float):
        if self._blocked:
            raise ValueError("Ваш аккаунт заблокирован")
        
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        
        self._balance += amount

    def withdraw(self, amount: float):
        if self._blocked:
            raise ValueError("Ваш аккаунт заблокирован")

        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        
        if amount > self._balance:
            raise ValueError("Недостаточно средств")
        
        self._balance -= amount