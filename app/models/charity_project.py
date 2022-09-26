from sqlalchemy import Column, String, Text

from app.models.base import BaseModel


class CharityProject(BaseModel):
    """
    Модель для представления благотворительного проекта в БД.
    Полный перечень полей таблицы:
    id — первичный ключ;
    name — обязательное уникальное название проекта;
    description — обязательное описание проекта;
    full_amount — требуемая сумма;
    invested_amount — внесённая сумма;
    fully_invested — булево поле, статус проекта (собраны ли средства);
    create_date — дата создания проекта;
    close_date — дата закрытия проекта
    """

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
