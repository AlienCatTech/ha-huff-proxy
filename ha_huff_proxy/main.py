import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from ha_huff_proxy.api import proxy, upload
from ha_huff_proxy.config import BASE_DIR
from ha_huff_proxy.logger import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

app.include_router(upload.router, tags=["upload"])
app.include_router(proxy.router, tags=["proxy"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
