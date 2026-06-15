from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


async def rfc_7807_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "code": "HTTP_ERROR",
            "field": None,
        },
    )


async def validation_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    field = None
    if errors and len(errors) > 0:
        field = ".".join(str(p) for p in errors[0].get("loc", [])) if errors[0].get("loc") else None
    return JSONResponse(
        status_code=422,
        content={
            "detail": str(errors[0]["msg"]) if errors else "Error de validación",
            "code": "VALIDATION_ERROR",
            "field": field,
        },
    )
