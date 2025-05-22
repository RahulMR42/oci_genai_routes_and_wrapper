import os
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import genai
from resources.basic_auth import Auth



VERSION = '0.0.0'

config = {
    "title": "GenaiCustomRoutes",
    "description": "Custom routes for Genai",
    "version": VERSION,
}


app = FastAPI(**config)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(genai.router)

@app.get("/")
async def health():
    return {"message": "Hello Wish you Good Health!"}

def load_app():
    port = os.getenv('PORT', default=5000)
    validate_app_password = os.getenv("APP_PASSWORD_VALIDATION", True)
    auth_handler = Auth(validate=validate_app_password)
    auth_handler.validate_env()
    uvicorn.run("src.app:app", host="0.0.0.0", port=port, reload=True)

if __name__ == "__main__":
    load_app