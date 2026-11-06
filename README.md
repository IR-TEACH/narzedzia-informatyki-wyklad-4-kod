# MiniLib

Mała biblioteka: katalog książek, czytelnicy, przypomnienia o zwrocie.

Uruchomienie:

```
uv run minilib                              # katalog książek
uv run python -m minilib.notify             # przypomnienie SMS
uv run uvicorn minilib.api:app --reload     # API: http://127.0.0.1:8000/docs
```

Tokeny testowe API: `token-anna`, `token-jan`.
