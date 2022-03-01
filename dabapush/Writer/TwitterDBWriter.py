from .Writer import Writer
from ...smo_database import DB_Manager, Twitter_Data

class TwitterDBWriter(Writer):
    """ """

    def __init__(self, config):
        super().__init__()
        
        self.initialize_db = DB_Manager(config)
        self.engine = self.initialize_db.create_connection()
        self.twitter_initializer = Twitter_Data(self.engine)
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

        self.twitter_initializer.twitter_insert(data)
    
    def close_local_session(self):
        
        self.twitter_initializer.close_local_session()