from .Writer import Writer
from ..Configuration.DBWriterConfiguration import DBWriterConfiguration

# from ...smo_database import DB_Manager, Instagram_Data
smo_database = __import__("smo-database")


class InstagramDBWriter(Writer):
    """ """

    def __init__(self, config):
        super().__init__()

        self.initialize_db = smo_database.DB_Manager(config)
        self.engine = self.initialize_db.create_connection()
        self.instagram_initializer = smo_database.Instagram_Data(self.engine)
        self.instagram_initializer.create_local_session()

    def persist(self):
        """

        Parameters
        ----------
        Returns
        -------

        """
        data = self.buffer
        self.buffer = []

        self.instagram_initializer.insta_insert(data)

    def __del__(self):
        print("Session and Connection Terminated")


class InstagramDBWriterConfiguration(DBWriterConfiguration):
    yaml_tag = "!dabapush:InstagramDBWriterConfiguration"

    def __init__(
        self,
        name,
        id=None,
        chunk_size: int = 2000,
        user: str = "postgres",
        password: str = "password",
        dbname: str = "public",
        host: str = "localhost",
        port: int = 5432,
    ) -> None:
        super().__init__(name, id, chunk_size, user, password, dbname, host, port)

    def get_instance(self):
        """ """
        return InstagramDBWriter(self)
