class UserDetails:
    def __init__(self, id_, username, scope):
        self.id = id_
        self.username = username
        self.scope = scope

    @staticmethod
    def build():
        return UserDetails(None, None, None)
