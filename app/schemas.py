from pydantic import BaseModel


class Secret(BaseModel):
    body: str
    phrase: str


class SecretCreated(Secret):
    secret_key: str
