from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from . import user

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)


class LoginParam(BaseModel):
    username: str
    password: str


@router.post('/login')
async def login(param: LoginParam):
    res_user = await user.get_user_by_id(username=param.username)
    if res_user and param.password is res_user['password']:
        return res_user
    else:
        raise HTTPException(status_code=401, detail='username or password incorrect')


