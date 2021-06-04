from fastapi import FastAPI
from .routers import user, auth, machine_learning
import tensorflow as tf
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(machine_learning.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def root():
    return {"message": "Hello World"}


@app.get('/check_gpu')
def check_gpu():
    gpu = len(tf.config.list_physical_devices('GPU'))
    return {'message': f'Num GPUs Available: {gpu}'}
