from datetime import timedelta

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm

from . import user as User
from ..dependencies import create_access_token, credentials_exception, ACCESS_TOKEN_EXPIRE_MINUTES, extract_jwt

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)


@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    res_user = await User.find_user(username=form_data.username)
    if res_user is not None and form_data.password == res_user['password']:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"username": form_data.username}, expires_delta=None
        )
        return {"access_token": access_token}
    else:
        raise credentials_exception


@router.get('/testSecurePath')
async def get_user_by_username(user=Depends(extract_jwt)):
    return user
