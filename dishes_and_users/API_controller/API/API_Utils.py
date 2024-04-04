from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse

from core.config import AUTHOR, VERSION
from data_access.Data import Data

router = APIRouter()
data_instance: Data | None = None


def setup_routes(app):
    """
    Set up routes for the API.

    Args:
        app: The FastAPI application instance.
    """
    app.include_router(router)


def data_transmission(data: Data):
    """
    Transmit the data context to the database.

    Args:
        data (Data): The data context to transmit.
    """
    global data_instance
    if data_instance is None:
        data_instance = data


@router.get("/")
def read_root():
    """
    Root endpoint to welcome users to the Users and Dishes API.

    Returns:
        dict: A welcome message along with version and creator details.
    """
    return {"message": "Welcome to the Users and Dishes API",
            "version": VERSION,
            "Creator": AUTHOR}


@router.post("/auth")
async def auth(request: Request):
    """
    Endpoint to authenticate users.

    Args:
        request (Request): The incoming request containing user credentials.

    Returns:
        dict: A message indicating successful authentication.

    Raises:
        HTTPException: If an error occurs during authentication.
    """
    try:
        json = await request.json()
        login = json["login"]
        password = json["password"]
        resultat = data_instance.ORM("AUTHENTICATE", credentials=[login, password])
        if resultat is True:
            return {"message": "Good credentials"}

    except Exception as e:
        raise HTTPException(status_code=412, detail=str(e))


@router.options("/auth")
async def options_root():
    """
    Endpoint to provide OPTIONS method for authentication.

    Returns:
        JSONResponse: A JSON response with allowed methods and headers.
    """
    allowed_methods = ["POST", "OPTIONS"]
    headers = {
        "Allow": ", ".join(allowed_methods)
    }
    return JSONResponse(content=None, headers=headers)
