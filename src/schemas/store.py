# from datetime import datetime
#
# from pydantic import BaseModel
#
#
# class TunedModel(BaseModel):
#     class Config:
#         from_attributes = True
#
#
# class ManufacturerGetSchema(TunedModel):
#     id: int
#     title: str
#     description: str | None = None
#     city: str
#     street: str
#     house: str
#     office: str | None = None
#     metro_station: str | None = None
#     website: str | None = None
#     # status: str
#     registration_date: datetime
#
#
# class ManufacturerPostSchema(TunedModel):
#     title: str
#     description: str | None = None
#     city: str
#     street: str
#     house: str
#     office: str | None = None
#     metro_station: str | None = None
#     website: str | None = None
#     # status: str
