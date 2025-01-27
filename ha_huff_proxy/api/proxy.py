import logging
from fastapi import APIRouter, Request, Response
import httpx

from ha_huff_proxy.common import is_valid_ipv4

router = APIRouter()
logger = logging.getLogger(__name__)


async def handle_proxy_request(
    request: Request, response: Response, hostname: str, path: str = ""
):
    if not is_valid_ipv4(hostname):
        part = hostname
        hostname = request.cookies.get("proxy_host")
        target_url = f"http://{hostname}/{part}/{path}".rstrip("/")

    else:
        target_url = f"http://{hostname}/{path}".rstrip("/")

    # Get the request body and headers
    body = await request.body()
    headers = dict(request.headers)
    headers.pop("host", None)

    async with httpx.AsyncClient() as client:
        logger.info(f"{request.url} >>>>>>> {target_url}")
        server_response = await client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            content=body,
            params=request.query_params,
        )

        headers = dict(server_response.headers)
        if "content-encoding" in headers:
            headers.pop("content-encoding")
        if "content-length" in headers:
            headers.pop("content-length")

        if is_valid_ipv4(hostname):
            headers.setdefault("Set-Cookie", f"proxy_host={hostname}; Path=/")

        return Response(
            content=server_response.content.decode(),
            status_code=server_response.status_code,
            headers=headers,
        )


@router.api_route(
    "/proxy/{hostname}/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
)
async def proxy_request(request: Request, response: Response, hostname: str, path: str):
    return await handle_proxy_request(request, response, hostname, path)
