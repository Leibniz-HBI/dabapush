from .Writer import Writer


class TwitterDBWriter(Writer):
    """ """

    def __init__(self, config):
        super().__init__()
        
        self.initialze_db = DBManager(config)
        self.engine = self.initialize_db.create_connection()
        self.twitter_initializer = Twitter_Data(self.engine)
        self.session = self.twitter_initializer.create_local_session()

    def persist(self):
        """

        Parameters
        ----------
        Returns
        -------

        """
        data = self.buffer
        self.buffer = []

        self.twitter_initializer.fb_insert(data)