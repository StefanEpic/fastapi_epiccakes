import enum


class ActiveStatus(enum.Enum):
    active = "Действующий"
    inactive = "Недействующий"


class JobTitle(enum.Enum):
    intern = "Стажер"
    junior = "Младший специалист"
    middle = "Специалист"
    senior = "Ведущий специалист"


class ProductType(enum.Enum):
    biscuit = "Бисквитные"
    sandy = "Песочные"
    puff = "Слоеные"
    waffle = "Вафельные"
    air = "Воздушные"
    tiny = "Крошковые"
    custards = "Заварные"


class OrderDelivery(enum.Enum):
    delivery = "Доставка"
    pickup = "Самовывоз"


class OrderPay(enum.Enum):
    cash = "Наличными"
    card = "Банковской картой"


class OrderStatus(enum.Enum):
    processing = "В работе"
    done = "Выполнено"
