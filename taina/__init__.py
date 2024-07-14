__version__ = "0.0.1a1"

import fastapi
import fastapi.responses

app = fastapi.FastAPI()


@app.get("/")
def redirect_to_docs():
    return fastapi.responses.RedirectResponse("/docs")
