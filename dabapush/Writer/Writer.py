from datetime import datetime
from typing import Dict
import pandas as pd
import abc
import threading
from loguru import logger as log
from pathlib import Path

class Writer(object):
    """ """

    # TODO: get chunksize from config
    def __init__(self):
        # TODO: schema schould not be here and should not be hard-coded!!!!!!!!!!!!1 
        self.schema = [
            'source',
            'created_at',
            'lang',
            'reply_settings',
            'referenced_tweets',
            'possibly_sensitive',
            'author_id',
            'id',
            'text',
            'conversation_id',
            'public_metrics.retweet_count',
            'public_metrics.reply_count',
            'public_metrics.like_count',
            'public_metrics.quote_count',
            'entities.mentions',
            'in_reply_to_user_id',
            'entities.urls',
            'entities.hashtags',
            'attachments.media_keys',
            'context_annotations'
        ]
        self.buffer = pd.DataFrame()
        # if (self.mp == True):
        self.lock = threading.Lock()
        # TODO: remove path attribute from from this class
        self.path = Path(f'{datetime.strftime(datetime.now(), "%Y%m%d_%H%M")}_twacapic.csv')
        # create output file
        with self.path.open('w') as file:
            file.writelines(f'{",".join(self.schema)}\n')
        # TODO: use this chunkSize, or rather read chunkSize from configuration
        self.chunkSize = 100

    def __del__(self):
        # flush buffer before destruction
        self.persist(len(self.buffer))

    def write(self, df: pd.DataFrame):
        """

        Args:
          df: pd.DataFrame: 

        Returns:

        """
        # if (self.mp == True):
        with self.lock:
            self.buffer = pd.concat([self.buffer, df], ignore_index=True, sort=False)
            log.info(f'Buffer now contains {len(self.buffer)} records for thread {id}.')

            # Call write persistance loop to empty buffer
            while (len(self.buffer) > self.chunkSize):
                self.persist(len(self.buffer))
    # else:
        #     self.buffer = pd.concat([self.buffer, df], ignore_index=True, sort=False)
        #     log.info(f'Buffer now contains {len(self.buffer)} records for thread {id}.')

        #     # Call write persistance loop to empty buffer
        #     while (len(self.buffer) > self.chunkSize):
        #         self.persist(len(self.buffer))

    @abc.abstractmethod
    def persist(self, chunkSize: int) -> None:
        """

        Args:
          chunkSize: int: 

        Returns:

        """
        return None
