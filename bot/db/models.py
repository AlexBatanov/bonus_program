from datetime import datetime
from typing import List
from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class Employee(Base):
    "Модель сотрудника"

    __tablename__ = "employees"
    
    name: Mapped[str] = mapped_column(String(30))
    telegram_id: Mapped[int] = mapped_column(unique=True)
    date_registered: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    is_admin: Mapped[bool] = mapped_column(default=False)
    buyers: Mapped[List["Buyer"]] = relationship()


class Buyer(Base):
    "Модель клиента (покупателя)"

    __tablename__ = "buyers"
    
    name: Mapped[str] = mapped_column(String(30))
    number: Mapped[str] = mapped_column(String(11), unique=True)
    date_registered: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    date_aplication: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    bonus_points: Mapped[int] = mapped_column(default=0)
    films: Mapped[str] = mapped_column()
    cheque: Mapped[int] = mapped_column(default=0)
    last_cheque: Mapped[int] = mapped_column(default=0)
    count_aplications: Mapped[int] = mapped_column(default=0)
    last_employee: Mapped[int] = mapped_column(ForeignKey("employees.telegram_id"))


class BonusPoint(Base):
    "Модель бонусов"
    
    __tablename__ = 'Bonus_point'

    name: Mapped[str] = mapped_column(String(30), unique=True)
    percent: Mapped[int] = mapped_column(default=10)


