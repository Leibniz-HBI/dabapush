from .Writer import Writer
from ...smo_database import DB_Manager, Instagram_Data

class InstagramDBWriter(Writer):
    """ """

    def __init__(self, config):
        super().__init__()
        
        self.initialize_db = DB_Manager(config)
        self.engine = self.initialize_db.create_connection()
        self.instagram_initializer = Instagram_Data(self.engine)
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