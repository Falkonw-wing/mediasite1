# from sqlalchemy import Column, Integer, String, Float, Text
# from app.database import Base  # Используем Base, который был определен в app/database.py
#
# class User(Base):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True, nullable=False)
#     hashed_password = Column(String, nullable=False)
#     role = Column(String, default="user")  # Роли: 'user', 'admin'
#
# class Item(Base):
#     __tablename__ = "items"
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True, nullable=False)
#     description = Column(Text)
#     price = Column(Float, nullable=False)
