# api/v1/common/association_tables.py
from sqlalchemy import Table, Column, Integer, ForeignKey
from app.entities.base import Base

company_users = Table(
    "companyUsers",
    Base.metadata,
    Column('id',Integer,primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("company_id", Integer, ForeignKey("companies.id"))
)