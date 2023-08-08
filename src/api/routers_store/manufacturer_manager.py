# from typing import List
#
# from fastapi import APIRouter, Depends
# from sqlmodel import Session
#
# from db.db import get_session
# from models.store.manufacturer_manager import ManufacturerManagerRead, ManufacturerManagerCreate, \
#     ManufacturerManagerUpdate
# from repositories.store import ManufacturerManagerRepository
#
# router = APIRouter(
#     prefix="/manufacturer_managers",
#     tags=["Manufacturer Managers"],
# )
#
#
# @router.get('', response_model=List[ManufacturerManagerRead])
# async def get_manufacturers(session: Session = Depends(get_session)):
#     return await ManufacturerManagerRepository(session).get_list()
#
#
# @router.get('/{manager_id}', response_model=ManufacturerManagerRead)
# async def get_manufacturer(manufacturer_id: int, session: Session = Depends(get_session)):
#     return await ManufacturerManagerRepository(session).get_one(manufacturer_id)
#
#
# @router.post('', response_model=ManufacturerManagerRead)
# async def add_manufacturer(manufacturer: ManufacturerManagerCreate, session: Session = Depends(get_session)):
#     return await ManufacturerManagerRepository(session).add_one(manufacturer)
#
#
# @router.patch('/{manager_id}', response_model=ManufacturerManagerRead)
# async def patch_manufacturer(manufacturer_id: int, manufacturer: ManufacturerManagerUpdate,
#                              session: Session = Depends(get_session)):
#     return await ManufacturerManagerRepository(session).edit_one(manufacturer_id, manufacturer)
#
#
# @router.delete('/{manager_id}')
# async def patch_manufacturer(manufacturer_id: int, session: Session = Depends(get_session)):
#     return await ManufacturerManagerRepository(session).delete_one(manufacturer_id)
