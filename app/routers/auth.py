from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import user

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)


class LoginParam(BaseModel):
    username: str
    password: str


@router.post('/login')
async def login(param: LoginParam):
    res_user = user.getUser(username=param.username)
    if res_user:
        return res_user
    else:
        raise HTTPException(status_code=401, detail='username or password incorrect')


