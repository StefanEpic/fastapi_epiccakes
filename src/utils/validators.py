from string import punctuation

from fastapi import Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from db.db import get_session


def name_valid(name):
    if not name.isalpha():
        raise ValueError("Error. Invalid value for name field")
    return name


def email_valid(email):
    if "@" not in email:
        raise ValueError("Error. Invalid value for email field")
    return email


def phone_valid(phone):
    p = punctuation.replace('+', '')
    if phone.isalpha() or len(set(p) & set(phone)) > 0:
        raise ValueError("Error. Invalid value for phone field")
    return phone


def rating_valid(rating):
    if rating < 0 or rating > 5:
        raise ValueError("Error. Invalid value for rating field")
    return rating
