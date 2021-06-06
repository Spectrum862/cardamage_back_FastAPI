from fastapi import APIRouter

router = APIRouter(
    prefix='/user',
    tags=['user']
)

mockUser = {
    'naiA': {
        'username': 'naiA',
        'name': 'a',
        'password': '1234'
    },
    'naiB': {
        'username': 'naiB',
        'name': 'b',
        'password': '1234'
    }
}


async def find_user(username:str):
    if username in mockUser:
        return mockUser[username]


@router.get('/{username}')
async def get_user_by_username(username: str):
    return find_user(username=username)


