from .user import User


class Admin(User):
    def __init__(self, login: str, password: str):
        super().__init__(login, password, balance=0.0)

    def ban(self, user: User):
        if user is self:
            raise ValueError("Нельзя забанить самого себя")
        
        user.blocked = True

    def unban(self, user: User):
        user.blocked = False