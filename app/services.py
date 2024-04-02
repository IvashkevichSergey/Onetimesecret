import random

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas
from app.models import Secret
from cryptography.fernet import Fernet
from app.config import settings


fernet_key = Fernet(settings.FERNET_KEY)


def generate_random_key() -> str:
    """Function generates random 7 digits number
    Returns
    -------
    str
        A string that contains generated random number
    """
    random_key = [str(random.randint(0, 9)) for _ in range(7)]
    return ''.join(random_key)


def create_new_secret(session: AsyncSession,
                      secret: schemas.Secret,
                      secret_key: str) -> Secret:
    """Create an instance of new Secret. Function uses cryptography
    for encryption by Fernet class
    Parameters
    ----------
    secret : Secret
        An instance of pydantic class Secret
    secret_key : str
        A number associated with a secret
    session : AsyncSession
        An instance of _asyncio.AsyncSession class

    Returns
    -------
    Secret
        An instance of a Secret class
    """
    secret_body = fernet_key.encrypt(bytes(secret.body, encoding="utf-8"))
    secret_phrase = fernet_key.encrypt(bytes(secret.phrase, encoding="utf-8"))
    new_secret = Secret(
        body=secret_body,
        phrase=secret_phrase,
        secret_key=secret_key
    )
    session.add(new_secret)
    return new_secret


async def get_secret_from_db(session: AsyncSession,
                             secret_key: str,
                             phrase: str) -> bytes | None:
    """Return a Secret instance body from database by a secret key
    and a code phrase and delete it from database at the same time
    Parameters
    ----------
    secret_key : str
        A number associated with a secret
    phrase : str
        A code phrase to get access to a secret
    session : AsyncSession
        An instance of _asyncio.AsyncSession class

    Returns
    -------
    bytes
        A secret from database if secret_key and phrase are correct.
        Otherwise None"""
    query = select(Secret).where(Secret.secret_key == secret_key)
    result = await session.execute(query)
    secret = result.scalar()
    if not secret:
        return None

    decrypted_phrase = fernet_key.decrypt(secret.phrase).\
        decode(encoding="utf-8")
    if secret and (phrase == decrypted_phrase):
        secret_id: int = secret.id
        query = delete(Secret).where(Secret.id == secret_id)
        await session.execute(query)
        await session.commit()
        return fernet_key.decrypt(secret.body)

    return None
