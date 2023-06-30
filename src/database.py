# from databases import Database
# from sqlalchemy import (
#     Boolean,
#     Column,
#     DateTime,
#     ForeignKey,
#     Identity,
#     Integer,
#     LargeBinary,
#     MetaData,
#     String,
#     Table,
#     create_engine,
#     func,
# )
# from sqlalchemy.dialects.postgresql import UUID

# from src.config import settings
# from src.constants import DB_NAMING_CONVENTION

# DATABASE_URL = settings.DATABASE_URL

# engine = create_engine(DATABASE_URL)
# metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)

# database = Database(DATABASE_URL, force_rollback=settings.ENVIRONMENT.is_testing)


# auth_user = Table(
#     "auth_user",
#     metadata,
#     Column("id", Integer, Identity(), primary_key=True),
#     Column("email", String, nullable=False),
#     Column("password", LargeBinary, nullable=False),
#     Column("is_admin", Boolean, server_default="false", nullable=False),
#     Column("created_at", DateTime, server_default=func.now(), nullable=False),
#     Column("updated_at", DateTime, onupdate=func.now()),
# )

# refresh_tokens = Table(
#     "auth_refresh_token",
#     metadata,
#     Column("uuid", UUID, primary_key=True),
#     Column("user_id", ForeignKey("auth_user.id", ondelete="CASCADE"), nullable=False),
#     Column("refresh_token", String, nullable=False),
#     Column("expires_at", DateTime, nullable=False),
#     Column("created_at", DateTime, server_default=func.now(), nullable=False),
#     Column("updated_at", DateTime, onupdate=func.now()),
# )

import os

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


class Database:
    def __init__(self):
        self.client = MongoClient(
            "mongodb+srv://huy8bit:ad853KqZsDfltWS1@cluster0.rn1ij5q.mongodb.net/?retryWrites=true&w=majority",
            server_api=ServerApi("1"),
        )
        try:
            self.client.admin.command("ping")
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    def get_collection(self, col):
        my_db = self.client["product"]
        return my_db[col]


database = Database()
