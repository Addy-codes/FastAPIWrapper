from fastapi import FastAPI
from app.routes import router as interactsh_router

app = FastAPI()

# Include the interact.sh routes
app.include_router(interactsh_router)
