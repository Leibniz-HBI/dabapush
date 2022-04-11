from ..Configuration.DBWriterConfiguration import DBWriterConfiguration
from .Writer import Writer

smo_database = __import__("smo-database")


class TwitterDBWriter(Writer):
    """ """

    def __init__(self, config: "TwitterDBWriterConfiguration"):
        super().__init__(config)

        self.initialize_db = smo_database.DB_Manager(
            config_dict={
                "user": config.dbuser,
                "password": config.dbpass,
                "localhost": config.hostname,
                "port": config.port,
                "dbname": config.dbname,
            }
        )
        self.engine = self.initialize_db.create_connection()
        self.twitter_initializer = smo_database.Twitter_Data(self.engine)
        self.twitter_initializer.create_local_session()

    def persist(self):
        """

        Parameters
        ----------
        Returns
        -------

        """
        data = self.buffer
        self.buffer = []

        [self.twitter_initializer.twitter_insert(_) for _ in data]
        self.twitter_initializer.local_session.commit()

    def __del__(self):
        print("Session and Connection Terminated")


class TwitterDBWriterConfiguration(DBWriterConfiguration):
    yaml_tag = "!dabapush:TwitterDBWriterConfiguration"

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
        return TwitterDBWriter(self)
