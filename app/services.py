import random

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas
from app.models import Secret


def generate_random_key() -> str:
    """Function generate random 7 digits number
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
    """Create an instance of new Secret
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
    # user_password = pwd_context.hash(user_data.password)
    new_secret = Secret(**secret.model_dump(), secret_key=secret_key)
    session.add(new_secret)
    return new_secret


async def get_secret_from_db(session: AsyncSession,
                             secret_key: str,
                             phrase: str) -> str | None:
    """Return a Secret instance name from database by a secret key
    and a code phrase and delete it at the same time
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
    str
        A secret from database if secret_key and phrase are corrects. Otherwise None"""
    query = delete(Secret).\
        where(
        (Secret.secret_key == secret_key)
        & (Secret.phrase == phrase)
    ).returning(Secret.body)
    result = await session.execute(query)
    await session.commit()
    return result.scalar()
