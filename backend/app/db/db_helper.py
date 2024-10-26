from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings


class DataBaseHelper:
    """Менеджер сессии к базе данных."""

    def __init__(
        self,
        db_uri,
        echo: bool = False,
    ) -> None:
        """Инициализирует асинхронный engine и создает фабрику сессий."""
        self.engine: AsyncEngine = create_async_engine(url=db_uri, echo=echo)
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine, expire_on_commit=False, autocommit=False, autoflush=False
        )

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Получение асинхронной сессии."""
        async with self.session_factory() as session:
            yield session

    async def dispose(self) -> None:
        """Утилизация Engine при завершении работы приложения."""
        await self.engine.dispose()


db_helper = DataBaseHelper(settings.db.database_uri, echo=settings.db.echo)
