from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json
import os

app = FastAPI()

FILE_PATH = os.getenv("FILE_NAME", "/repo/life.json")
API_TOKEN = os.getenv("API_TOKEN")

@app.get("/life")
async def read_life(authorization: str = Header(...)):
    if authorization != f"Bearer {API_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        with open(FILE_PATH, "r") as f:
            data = json.load(f)
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/life")
async def update_life(request: Request, authorization: str = Header(...)):
    if authorization != f"Bearer {API_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        wrapper = await request.json()
        # Robust fallback chain
        data = (
            wrapper.get("params", {})
                   .get("life", wrapper.get("params", {}))
                   or wrapper.get("file")
                   or wrapper
        )

        with open(FILE_PATH, "w") as f:
            json.dump(data, f, indent=2)

        return JSONResponse(content={"detail": "Update successful"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
