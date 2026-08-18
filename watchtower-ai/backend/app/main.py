import uvicorn
from fastapi import FastAPI
from app.core.config import settings
from app.api.v1 import uploads, users

app = FastAPI(title=settings.PROJECT_NAME, docs_url="/docs")

app.include_router(uploads.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(uploads.router, prefix="/api/v1/models", tags=["models"])

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
