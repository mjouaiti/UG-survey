# app/db.py

from enum import unique
import databases
import ormar
import sqlalchemy
import datetime

from .config import settings

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = "user"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=64)
    email: str = ormar.String(max_length=128, unique=True, nullable=False)
    major: str = ormar.String(max_length=64, unique=True, nullable=False)
    personal_statement: str = ormar.String(max_length=16384)
    active: bool = ormar.Boolean(default=True, nullable=False)
    created_at: datetime.datetime = ormar.DateTime(timezone=True, default=datetime.datetime.now())


class Conversation(ormar.Model):
    class Meta(BaseMeta):
        tablename = "conversation"

    id: int = ormar.Integer(primary_key=True)
    user_id: User = ormar.ForeignKey(User)
    speaker: str = ormar.String(max_length=32, unique=True)
    session: int = ormar.Integer()
    turn: int = ormar.Integer()
    transcript: str = ormar.String(max_length=512, unique=True)
    created_at: datetime.datetime = ormar.DateTime(timezone=True, default=datetime.datetime.now())



engine = sqlalchemy.create_engine(settings.db_url)
# metadata.drop_all(engine)

# metadata.create_all(engine)
