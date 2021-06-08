from datetime import timedelta

from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from .dependencies import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, Token
from .routers import user, auth, insurance, machine_learning
import tensorflow as tf
from starlette.middleware.cors import CORSMiddleware

from .routers.user import find_user

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(machine_learning.router)
app.include_router(insurance.router)
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


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    res_user = await find_user(username=form_data.username)
    if not res_user and res_user.password != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

