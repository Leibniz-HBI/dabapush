from .Writer import Writer

class FacebookDBWriter(Writer):
    """ """

    def __init__(self, config):
        super().__init__()
        
        self.initialze_db = DBManager(config)
        self.engine = self.initialize_db.create_connection()
        self.facebook_initializer = Facebook_Data(self.engine)
        self.session = self.facebook_initializer.create_local_session()

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