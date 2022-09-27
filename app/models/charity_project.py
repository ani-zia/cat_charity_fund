from sqlalchemy import Column, String, Text

from app.models.base import BaseModel


class CharityProject(BaseModel):
    """
    Модель для представления благотворительного проекта в БД
    """

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (f'CharityProject(name={self.name}, '
                f'full_amount={self.full_amount})')

    def __str__(self):
        return (f'Проект {self.name}, '
                f'необходимо собрать {self.full_amount}')
