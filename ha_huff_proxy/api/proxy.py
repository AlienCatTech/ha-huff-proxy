from fastapi import APIRouter, FastAPI, Request
import httpx
from fastapi.responses import StreamingResponse

router = APIRouter()

async def handle_proxy_request(request: Request, hostname: str, path: str = ""):
    # Construct the target URL
    target_url = f"http://{hostname}/{path}".rstrip("/")

    # Get the request body and headers
    body = await request.body()
    headers = dict(request.headers)
    headers.pop("host", None)

    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            content=body,
            params=request.query_params,
        )

        return StreamingResponse(
            response.iter_bytes(),
            status_code=response.status_code,
            headers=dict(response.headers),
        )


@router.api_route(
    "/proxy/{hostname}/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
)
async def proxy_request(request: Request, hostname: str, path: str):
    return await handle_proxy_request(request, hostname, path)


@router.api_route(
    "/proxy/{hostname}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
)
async def proxy_request_root(request: Request, hostname: str):
    return await handle_proxy_request(request, hostname)
