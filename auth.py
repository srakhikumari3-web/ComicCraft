"""Small request-validation helpers kept as a separate module for future auth.
ComicCraft intentionally has no user-account system in the supplied specification.
"""
from fastapi import HTTPException, status


def require_non_empty(value: str, field_name: str = "value") -> str:
    value = (value or "").strip()
    if not value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{field_name} cannot be empty.",
        )
    return value
