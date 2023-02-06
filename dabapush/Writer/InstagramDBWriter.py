"""The Instagram-DBWriter."""
from ..Configuration.DBWriterConfiguration import DBWriterConfiguration
from .Writer import Writer

smo_database = __import__("smo-database")


class InstagramDBWriter(Writer):
    """Persists data from Instagram."""

    def __init__(self, config: DBWriterConfiguration):
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

        for _ in data:
            self.instagram_initializer.insta_insert(_)

        self.instagram_initializer.local_session.commit()

    def __del__(self):
        print("Session and Connection Terminated")
        super().__del__()  # this triggers self.persits and must be called


class InstagramDBWriterConfiguration(DBWriterConfiguration):
    """Configuration for the InstagramDBWriter"""

    yaml_tag = "!dabapush:InstagramDBWriterConfiguration"

    def get_instance(self) -> InstagramDBWriter:  # pylint: disable=W0221
        return InstagramDBWriter(self)
