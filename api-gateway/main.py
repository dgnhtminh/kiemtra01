from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI(title="API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SERVICES = {
    "staff": "http://localhost:8001",
    "customer": "http://localhost:8002",
    "laptop": "http://localhost:8003",
    "mobile": "http://localhost:8004",
}

@app.api_route("/{service_name}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def gateway(service_name: str, path: str, request: Request):
    if service_name not in SERVICES:
        raise HTTPException(status_code=404, detail="Service not found")
        
    url = f"{SERVICES[service_name]}/{path}"
    
    # Read the body of the original request
    body = await request.body()
    
    # Forward the request to the target microservice
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=url,
                headers=dict(request.headers),
                content=body,
                params=dict(request.query_params)
            )
            # Return the response from the microservice
            return response.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Service unavailable: {exc}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
