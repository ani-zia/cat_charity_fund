from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import BaseModel


class Donation(BaseModel):
    """
    Модель для представления пожертвования в БД.
    Полный перечень полей таблицы:
    id — первичный ключ;
    user_id — id пользователя, сделавшего пожертвование;
    comment — необязательное поле комментария;
    full_amount — сумма пожертвования;
    invested_amount — сумма из пожертвования, которая распределена по проектам;
    fully_invested — булево поле, потрачено пожертвование или нет;
    create_date — дата пожертвования;
    close_date — дата, когда вся сумма пожертвования была потрачена
    """
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
