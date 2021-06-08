import random
import string
import time

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix='/insurance',
    tags=['Insurance']
)

insurance_data = {
    '74541987':{
        'insurance_id':'79815849181',
        'name':'นายศาลทูล ขุนสนิท',
        'car_brand':'Honda',
        'car_model':'Civic2019',
        'car_license':'กขค1234'
    },
    '51374897':{
        'insurance_id':'942159784154',
        'name':'นายกัตชาติ จรรยาบรรณ',
        'car_brand':'Toyota',
        'car_model':'Fortuner',
        'car_license':'หกย8521'
    }
}

class Insurance(BaseModel):
    insurance_id:str
    name:str
    car_brand:str
    car_model:str
    car_license:str


@router.get('/')
async def get_insurance_list():
    time.sleep(2)
    return insurance_data


@router.post('/add')
async def get_insurance_list(body: Insurance):
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
    insurance_data[random_str] = {
        'insurance_id': body.insurance_id,
        'name': body.name,
        'car_brand': body.car_brand,
        'car_model': body.car_model,
        'car_license': body.car_license
    }
    return insurance_data
