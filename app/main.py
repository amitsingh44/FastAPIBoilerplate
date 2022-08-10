from fastapi import FastAPI
from .routers import post

app = FastAPI()

@app.get('/')
def index():
    return {'message':'Hello World!'}

app.include_router(post.router)  