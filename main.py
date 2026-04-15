from fastapi import FastAPI
from src.interction.router import router as interaction_router
from src.like.router import router as like_router



app = FastAPI()
app.include_router(interaction_router)
app.include_router(like_router)

@app.get("/")
def health():
    return {"status": "Healthy"}