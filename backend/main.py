from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from core.logger import logger
import traceback

from models import *

from api.routes import auth, user, admin, exam

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://exam-platform-mvp.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== ROUTES =====
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(admin.router)
app.include_router(exam.router)


# ===== ROOT =====
@app.get("/")
def root():
    logger.info("Root endpoint hit")
    return {"message": "jarvis active"}


# ===== EXCEPTION HANDLERS =====
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"HTTP error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": exc.detail}
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    logger.error(traceback.format_exc())

    return JSONResponse(
        status_code=500,
        content={"success": False, "error": "Internal server error"}
    )