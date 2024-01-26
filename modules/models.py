from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, String, Integer, SmallInteger, Numeric, Boolean, DateTime, ForeignKey
from sqlalchemy.sql.expression import text

from modules.connection import engine


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False, index=True)
    login = Column(String(length=32), nullable=False, unique=True)
    psw = Column(String(length=255), nullable=False)
    access_level = Column(SmallInteger, default=1, server_default=text('1'))


class Customers(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False, index=True)
    name_cust = Column(String(length=32), nullable=False, unique=True)
    is_deleted = Column(Boolean, nullable=False,
                        default=False, server_default=text('False'))

    accounts = relationship("Accounts", back_populates="customer")


class Accounts(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, autoincrement=True,
                index=True, nullable=False)
    cust_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    account_number = Column(String(length=16), nullable=False, unique=True)
    is_deleted = Column(Boolean, nullable=False,
                        default=False, server_default=text('False'))
    date_deleted = Column(DateTime, nullable=True)
    amount = Column(Numeric(precision=10, scale=2),
                    nullable=False, default=10000, server_default=text('10000'))

    customer = relationship("Customers", back_populates="accounts")


Base.metadata.create_all(bind=engine)
