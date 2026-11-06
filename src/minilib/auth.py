"""Logowanie do API tokenem. W prawdziwej aplikacji: baza kont i hasła."""
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from minilib.member import Member

TOKENS = {
    "token-anna": Member("Anna Nowak", "anna.nowak@example.com"),
    "token-jan": Member("Jan Kowalski", "jan.kowalski@example.com"),
}


def current_member(
    cred: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> Member:
    member = TOKENS.get(cred.credentials)
    if member is None:
        raise HTTPException(401, "Nieznany token")
    return member
