from string import punctuation


def name_valid(name: str) -> str:
    if not name.isalpha():
        raise ValueError("Error. Invalid value for name field")
    return name


def email_valid(email: str) -> str:
    if "@" not in email:
        raise ValueError("Error. Invalid value for email field")
    return email


def phone_valid(phone: str) -> str:
    p = punctuation.replace('+', '')
    if phone.isalpha() or len(set(p) & set(phone)) > 0:
        raise ValueError("Error. Invalid value for phone field")
    return phone


def rating_valid(rating: int) -> int:
    if rating < 0 or rating > 5:
        raise ValueError("Error. Invalid value for rating field")
    return rating
