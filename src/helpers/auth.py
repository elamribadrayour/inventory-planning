import os

from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader


api_key_header_auth = APIKeyHeader(name="X-API-KEY", auto_error=False)


async def check(api_key_in_header: str = Security(api_key_header_auth)) -> None:
    """Check user authentication."""
    if api_key_in_header is None or len(api_key_in_header) == 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Empty credentials, provide a `X-API-KEY`",
        )

    if api_key_in_header == os.environ["API_KEY"]:
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )
