from string import digits, punctuation, ascii_letters


def var2str(var, vars_data = locals()):
    return [var_name for var_name in vars_data if id(var) == id(vars_data[var_name])][0]


def name_valid(self, key, name):
    if digits in name or punctuation in name:
        raise ValueError(f"invalid value for {var2str(name)} field")
    return name


def email_valid(self, key, email):
    if "@" not in email:
        raise ValueError(f"invalid value for {var2str(email)} field")
    return email


def phone_valid(self, key, phone):
    punctuation = punctuation.replace('-', '') 
    if ascii_letters in phone or punctuation in phone:
        raise ValueError(f"invalid value for {var2str(phone)} field")
    return phone


def rating_valid(self, key, rating):
    if rating < 0 or rating > 5:
        raise ValueError(f"invalid value for {var2str(rating)} field")
    return email
