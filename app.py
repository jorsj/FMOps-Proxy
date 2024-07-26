import google.auth.transport.requests
import httpx
from fastapi import FastAPI, Request, Response
from google.auth import default

app = FastAPI()

# Base URL for the OpenAI API
OPENAI_API_URL = "api.openai.com"
VERTEX_API_URL = "us-central1-aiplatform.googleapis.com"


@app.api_route("/openai/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_openai(path: str, request: Request):
    url = f"https://{OPENAI_API_URL}/{path}"
    headers = dict(request.headers)
    headers["host"] = f"{OPENAI_API_URL}"
    # TODO: Change the Authorization header to use the OpenAI API key
    data = await request.body()

    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=url,
            headers=headers,
            content=data,
            params=request.query_params,
        )

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
    )


@app.api_route(
    "/vertexai/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
)
async def proxy_vertex(path: str, request: Request):
    creds, _ = default()
    auth_req = google.auth.transport.requests.Request()
    creds.refresh(auth_req)

    url = f"https://{VERTEX_API_URL}/{path}"
    headers = dict(request.headers)
    headers["host"] = f"{VERTEX_API_URL}"
    headers["Authorization"] = f"Bearer {creds.token}"
    data = await request.body()

    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=url,
            headers=headers,
            content=data,
            params=request.query_params,
        )
        response.headers["content-encoding"] = response.headers[
            "content-encoding"
        ].replace("gzip", "identity")

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
