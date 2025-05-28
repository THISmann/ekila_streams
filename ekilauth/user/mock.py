from typing import Any


class MockEkilaUser:
    users = [
        {
            "id": 1,
            "username": "rbaudin",
            "first_name": "Romain",
            "last_name": "Baudin",
            "email": "rbaudin@ekila.fr",
        },
        {
            "id": 2,
            "username": "mpastor",
            "first_name": "Marc",
            "last_name": "Pastor-Abad",
            "email": "mpastor@ekila.fr",
        },
        {
            "id": 3,
            "username": "chumeau",
            "first_name": "Clement",
            "last_name": "Humeau",
            "email": "chumeau@ekila.fr",
        },
        {
            "id": 4,
            "username": "dramelet",
            "first_name": "Damien",
            "last_name": "Ramelet",
            "email": "dramelet@ekila.fr",
        },
        {
            "id": 5,
            "username": "lbopp",
            "first_name": "Lucas",
            "last_name": "Bopp",
            "email": "lbopp@ekila.fr",
        },
        {
            "id": 6,
            "username": "dbourdon",
            "first_name": "Dylan",
            "last_name": "Bourdon",
            "email": "dbourdon@ekila.fr",
        },
    ]

    @classmethod
    def get_users_by_client_id(cls, user_email: str) -> Any:
        users_by_email: dict = dict()
        for user in cls.users:
            if not users_by_email.get(user["email"]):
                users_by_email[user["email"]] = list()
            users_by_email[user["email"]].append(user)
        return users_by_email.get(user_email, list())

    @classmethod
    def get_user(cls) -> Any:
        return cls.users[0]


class MockEkilauthResponse:
    def __init__(self, data):
        self.data = data
        self.status_code = 200

    def json(self):
        return self.data

    def raise_for_status(self) -> bool:
        return True


class MockEkilauthRequest:
    @classmethod
    def get(cls, *args, **kwargs) -> MockEkilauthResponse:
        user_email = kwargs.get("params", dict()).get("email")
        if user_email:
            data = MockEkilaUser.get_users_by_client_id(user_email)
        else:
            data = MockEkilaUser.get_user()
        return MockEkilauthResponse(data)
