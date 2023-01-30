import enum
import os
from datetime import datetime

from sqlalchemy import (Column, Integer, String, create_engine, DateTime, ForeignKey, Enum)
from sqlalchemy.engine import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

DATABASE = {
    'drivername': os.getenv('DRIVERNAME'),
    'host': os.getenv('HOST'),
    'port': os.getenv('PORT'),
    'username': os.getenv('DB_USERNAME'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DATABASE_NAME')
}

# Connect string
DATABASE_URI = URL.create(**DATABASE)

DeclarativeBase = declarative_base()
metadata = DeclarativeBase.metadata
engine = create_engine(DATABASE_URI)


class User(DeclarativeBase):
    """
    Declarative representation of a table User
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    login = Column(String(80), unique=True, nullable=False)
    password = Column(String(20), nullable=False)
    created_on = Column(
        DateTime(timezone=True), nullable=False,
        default=datetime.now().strftime('%Y.%m.%dT%H:%M:%S'))
    updated_on = Column(
        DateTime(timezone=True), nullable=False,
        default=datetime.now().strftime('%Y.%m.%dT%H:%M:%S'),
        onupdate=datetime.now().strftime('%Y.%m.%dT%H:%M:%S'))
    balance = Column(Integer, nullable=False, default=0)


class OrderStatusEnum(enum.Enum):
    """
    Enum class for fixed order status selection field
    REGISTERED — the order has been registered, but no accrual has been made;
    INVALID — the order was not accepted for settlement, and the reward will not be credited;
    PROCESSING - calculation of accrual in the process;
    PROCESSED — accrual completed;
    """
    registered = 'REGISTERED'
    invalid = 'INVALID'
    processing = 'PROCESSING'
    processed = 'PROCESSED'


class Order(DeclarativeBase):
    """
    Declarative representation of a table Order.
    """
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    number = Column(String, nullable=False, unique=True)
    created_on = Column(
        DateTime(timezone=True), nullable=False,
        default=datetime.now().strftime('%Y.%m.%dT%H:%M:%S'))
    updated_on = Column(
        DateTime(timezone=True), nullable=False,
        default=datetime.now().strftime('%Y.%m.%dT%H:%M:%S'),
        onupdate=datetime.now().strftime('%Y.%m.%dT%H:%M:%S'))
    status = Column(Enum(OrderStatusEnum), nullable=False, default=OrderStatusEnum.registered)
    sum = Column(Integer, nullable=False, default=0)
    user = relationship('User', backref='orders')


class Withdraw(DeclarativeBase):
    """
    Declarative representation of a table Withdraw
    """
    __tablename__ = 'withdraws'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    order_number = Column(String, ForeignKey('orders.number'))
    accrual = Column(Integer, nullable=False, default=0)
    updated_on = Column(
        DateTime(timezone=True), nullable=False,
        default=datetime.now().strftime('%Y.%m.%dT%H:%M:%S'),
        onupdate=datetime.now().strftime('%Y.%m.%dT%H:%M:%S'))
    user = relationship('User', backref='withdraws')


if __name__ == '__main__':
    metadata.create_all(engine)
