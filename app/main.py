from fastapi import FastAPI, HTTPException, Request, Depends, Header
from fastapi.responses import PlainTextResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from app.git_utils import get_life_yaml, update_life_yaml
import os

API_TOKEN = os.getenv("API_TOKEN")

app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

def verify_token(authorization: str = Header(...)):
    expected = f"Bearer {API_TOKEN}"
    if authorization != expected:
        raise HTTPException(status_code=403, detail="Unauthorized")

@app.get("/life", response_class=PlainTextResponse)
@limiter.limit("10/minute")
def read_life(request: Request, token: str = Depends(verify_token)):
    try:
        return get_life_yaml()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/life", response_class=PlainTextResponse)
@limiter.limit("5/minute")
async def write_life(request: Request, token: str = Depends(verify_token)):
    try:
        new_content = await request.body()
        update_life_yaml(new_content.decode("utf-8"))
        return "Updated successfully"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
