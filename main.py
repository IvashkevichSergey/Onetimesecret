from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing_extensions import Annotated

from app import schemas
from app.database import get_session
from app.services import generate_random_key, create_new_secret, get_secret_from_db

app = FastAPI()


@app.post("/generate",
          description="Endpoint to generate a new secret",
          status_code=status.HTTP_201_CREATED,
          tags=["Secrets"])
async def create_secret(secret: schemas.Secret,
                        session: AsyncSession = Depends(get_session)) -> str:
    """Endpoint to generate a new secret"""
    secret_key = generate_random_key()
    create_new_secret(session, secret, secret_key)
    try:
        await session.commit()
        return f"Secret_key for you secret is {secret_key}"
    except IntegrityError:
        await session.rollback()


@app.post("/secrets/{secret_key}",
          description="Endpoint to get a secret by secret key and code phrase",
          status_code=status.HTTP_200_OK,
          tags=["Secrets"])
async def get_secret(secret_key: str,
                     phrase: Annotated[str, Body(embed=True)],
                     session: AsyncSession = Depends(get_session)) -> dict:
    """Endpoint to get a secret"""
    secret = await get_secret_from_db(session, secret_key, phrase)
    if not secret:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid secret key or code phrase")
    return {"Secret": secret}
