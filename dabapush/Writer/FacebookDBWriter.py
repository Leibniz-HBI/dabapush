from ..Configuration.DBWriterConfiguration import DBWriterConfiguration
from .Writer import Writer

# from ...smo_database import DB_Manager, Facebook_Data
smo_database = __import__("smo-database")


class FacebookDBWriter(Writer):
    """ """

    def __init__(self, config):

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
        self.facebook_initializer = smo_database.Facebook_Data(self.engine)
        self.facebook_initializer.create_local_session()

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
            self.facebook_initializer.fb_insert(_)
            
        self.facebook_initializer.local_session.commit()

    def __del__(self):
        print("Session and Connection Terminated")
        super().__del__() # this triggers self.persits and must be called

class FacebookDBWriterConfiguration(DBWriterConfiguration):
    """Configuration for the FacebookDBWriter
    """
    yaml_tag = "!dabapush:FacebookDBWriterConfiguration"
    class_instance = FacebookDBWriter

    def get_instance(self) -> FacebookDBWriter:
        return FacebookDBWriter(self)