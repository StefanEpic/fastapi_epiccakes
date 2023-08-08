from string import digits, punctuation, ascii_letters


def get_str(n):
    return [k for k,v in locals().iteritems() if v == n][0]


def name_valid(self, key, name):
    if digits in name or punctuation in name:
        raise ValueError(f"invalid value for {get_str(name)} field")
    return name


def email_valid(self, key, email):
    if "@" not in email:
        raise ValueError(f"invalid value for {get_str(email)} field")
    return email


def phone_valid(self, key, phone):
    punctuation = punctuation.replace('-', '') 
    if ascii_letters in phone or punctuation in phone:
        raise ValueError(f"invalid value for {get_str(phone)} field")
    return phone


def rating_valid(self, key, rating):
    if rating < 0 or rating > 5:
        raise ValueError(f"invalid value for {get_str(rating)} field")
    return email
