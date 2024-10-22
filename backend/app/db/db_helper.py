from sqlalchemy.ext.asyncio import create_async_engine


class DBHelper:
    """Менеджер сессии к базе данных."""

    def __init__(self, db_uri):
        self.db_uri = db_uri
        self.engine = create_async_engine(self.db_uri)
