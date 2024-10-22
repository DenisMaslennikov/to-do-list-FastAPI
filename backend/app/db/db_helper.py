
class DBHelper:
    """Менеджер сессии к базе данных."""

    def __init__(self, db_uri):
        self.db_uri = db_uri
