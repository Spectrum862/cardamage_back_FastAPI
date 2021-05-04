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


def getUser(username: str):
    if username in mockUser:
        return mockUser[username]
    else:
        return None


@router.get('/{username}')
async def get_user_by(username: str):
    if username in mockUser:
        return mockUser[username]

