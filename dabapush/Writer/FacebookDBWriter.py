from .Writer import Writer
from ...smo_database import DB_Manager

class FacebookDBWriter(Writer):
    """ """

    def __init__(self, config):
        super().__init__()
        
        self.initialze_db = DB_Manager(config)
        self.engine = self.initialize_db.create_connection()
        self.facebook_initializer = Facebook_Data(self.engine)
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

    def close_local_session(self):
        self.facebook_initializer.close_local_session()