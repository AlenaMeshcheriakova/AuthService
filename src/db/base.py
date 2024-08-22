import datetime
import uuid
from typing import Annotated

from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import text, String, types

str_256 = Annotated[str,200]
class Base(DeclarativeBase):

    type_annotation_map = {
        str_256: String(200)
    }
    def get_intpk(self):
        intpk = Annotated[uuid.UUID, mapped_column(types.Uuid, primary_key=True)]
        return intpk

    def get_created_at(self):
        created_at = Annotated[datetime.datetime, mapped_column(
            server_default=text("TIMEZONE('utc', now())")
        )]
        return created_at

    def get_updated_at(self):
        updated_at = Annotated[datetime.datetime, mapped_column(
                server_default=text("TIMEZONE('utc', now())"),
                onupdate=datetime.datetime.now,
            )]
        return updated_at

    def __repr__(self) -> str:
        cols = []
        for col in self.__table__.columns.keys():
            cols.append(f"{col} = {getattr(self, col)}")
        return f"<{self.__class__.__name__} {', '.join(cols) }>"
