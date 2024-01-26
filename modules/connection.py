from modules.security import dbname_app, user_app, password_app, host_app, port_app

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


# Атрибут подключения для движка SQLAlchemy.
DATABASE_URL = f'postgresql+psycopg2://{
    user_app}:{password_app}@{host_app}:{port_app}/{dbname_app}'

# Создаём движок SQLAlchemy.
engine = create_engine(DATABASE_URL, echo=True)

# Создаем класс последующих сессий, на основе которого будут создаваться разовые экземпляры для разовых подключений.
Session = sessionmaker(bind=engine)
