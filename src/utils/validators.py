from string import digits, punctuation, ascii_letters


def name_valid(self, key, name):
    if digits in name or punctuation in name:
        raise ValueError("Error. Invalid value for name field")
    return name


def email_valid(self, key, email):
    if "@" not in email:
        raise ValueError("Error. Invalid value for email field")
    return email


def phone_valid(self, key, phone):
    punctuation = punctuation.replace('-', '') 
    if ascii_letters in phone or punctuation in phone:
        raise ValueError("Error. Invalid value for phone field")
    return phone


def rating_valid(self, key, rating):
    if rating < 0 or rating > 5:
        raise ValueError("Error. Invalid value for rating field")
    return rating
