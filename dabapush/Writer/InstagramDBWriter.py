from .Writer import Writer
from ...smo-database

class InstagramDBWriter(Writer):
    """ """

    def __init__(self, config):
        super().__init__()
        
        self.initialze_db = DBManager(config)
        self.engine = self.initialize_db.create_connection()
        self.instagram_initializer = Instagram_Data(self.engine)
        self.session = self.instagram_initializer.create_local_session()

    def persist(self):
        """

        Parameters
        ----------
        Returns
        -------

        """
        data = self.buffer
        self.buffer = []

        self.instagram_initializer.fb_insert(data)