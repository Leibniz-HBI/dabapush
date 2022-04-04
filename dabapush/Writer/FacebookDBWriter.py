from typing_extensions import Self
from ..Configuration.WriterConfiguration import WriterConfiguration
from .Writer import Writer
# from ...smo_database import DB_Manager, Facebook_Data
smo_database = __import__('smo-database')
class FacebookDBWriter(Writer):
    """ """

    def __init__(self, config):
        
        self.initialize_db = smo_database.DB_Manager(config)
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

        self.facebook_initializer.fb_insert(data)

    def __del__(self):
        print("Session and Connection Terminated")

class FacebookDBWriterConfiguration(WriterConfiguration):
    yaml_tag = '!dabapush:FacebookDBWriterConfiguration'

    def get_instance(self):
        """ """
        return FacebookDBWriter(Self)