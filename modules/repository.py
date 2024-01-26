from modules.connection import Session, engine
from modules.models import Accounts, Customers
from sqlalchemy import and_
from sqlalchemy.sql import func


def get_all_accounts(_is_deleted=False):
    with Session(autoflush=False, bind=engine) as db:
        accounts = db.query(Accounts).filter(
            Accounts.is_deleted == _is_deleted).all()
        return accounts


def get_customer_by_id(_id):
    with Session(autoflush=False, bind=engine) as db:
        customer = db.query(Customers).filter(
            and_(Customers.id == _id, Customers.is_deleted == False)).first()
    return customer


def get_accounts_by_cust_id(_id):
    with Session(autoflush=False, bind=engine) as db:
        accounts = db.query(Accounts).filter(
            and_(Accounts.cust_id == _id, Accounts.is_deleted == False)).all()
    return accounts


def get_max_account_number():
    with Session(autoflush=False, bind=engine) as db:
        max_acc_num = db.query(func.max(Accounts.account_number)).scalar()
    return max_acc_num


def add_accounts(_account_add):
    with Session(autoflush=False, bind=engine) as db:
        db.add(_account_add)
        db.commit()


def get_account_by_number(_account_number):
    with Session(autoflush=False, bind=engine) as db:
        account = db.query(Accounts).filter(
            and_(Accounts.account_number == _account_number, Accounts.is_deleted == False)).first()
    return account


def del_account(_account_number):
    with Session(autoflush=False, bind=engine) as db:
        account = db.query(Accounts).filter(
            Accounts.account_number == _account_number).first()
        if account is not None:
            account.is_deleted = True
            db.commit()


def update_account_balance(_account_number, _new_balance):
    with Session(autoflush=False, bind=engine) as db:
        account = db.query(Accounts).filter(
            Accounts.account_number == _account_number).first()
        if account is not None:
            account.amount = _new_balance
            db.commit()
