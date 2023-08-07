from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from db.db import get_session
from models.store import ManufacturerRead, Manufacturer
from repositories.store import ManufacturerRepository

router = APIRouter(
    prefix="/manufacturers",
    tags=["Manufacturer"],
)


@router.get('', response_model=List[ManufacturerRead])
async def get_manufacturers(session: Session = Depends(get_session)):
    manufacturers = await ManufacturerRepository(session).get_list()
    return manufacturers


#
# @router.post('', response_model=ManufacturerRead)
# async def add_manufacturer(manufacturer: ManufacturerRead):
#     manufacturer = await ManufacturerRepository().add_one(manufacturer)
#     return manufacturer

# @router.get('/{manufacturer_id}')
# async def get_manufacturer(manufacturer_id: int):
#     manufacturers = await ManufacturerRepository().get_one(id=manufacturer_id)
#     return manufacturers
#
#
# @router.patch('/{manufacturer_id}')
# async def patch_manufacturer(manufacturer_id: int, manufacturer):
#     manufacturer = manufacturer.model_dump()
#     manufacturer = await ManufacturerRepository().edit_one(manufacturer, id=manufacturer_id)
#     return manufacturer
#
#
# @router.delete('/{manufacturer_id}')
# async def patch_manufacturer(manufacturer_id: int):
#     manufacturer = await ManufacturerRepository().delete_one(manufacturer_id)
#     return manufacturer
