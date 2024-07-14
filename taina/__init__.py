__version__ = "0.0.1a1"

import contextlib

import fastapi
import fastapi.responses

from . import endpoints
from .core import config
from .core import postgres


@contextlib.asynccontextmanager
async def lifespan(_):
    await postgres.connect(config.postgres.url)
    yield
    await postgres.disconnect()


app = fastapi.FastAPI(lifespan=lifespan)
app.include_router(endpoints.router)


@app.get("/")
def redirect_to_docs():
    return fastapi.responses.RedirectResponse("/docs")
