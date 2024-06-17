from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from config import settings

engine = create_async_engine(settings.get_database_url)
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class ValueOrm(Base):
    __tablename__ = "values"

    id: Mapped[int] = mapped_column(primary_key=True)
    core_value: Mapped[str]
    user_id: Mapped[str]



