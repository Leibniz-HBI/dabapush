from datetime import date
from math import floor
from random import random
from typing import Dict, List

class Tweet(object):
    
    def __init__(self, retweet: bool = False, quoted: bool = False) -> None:
        self.id = floor(random() * 1e10)
        self.text = "Nothing to see hehe"
        self.user = User()
        self.retweeted_tweet = Tweet() if retweet is True else None
        self.quoted_tweet = Tweet() if quoted is True else None

    def to_v1(self) -> Dict:
        return {
            "id": self.id,
            "text": self.text,
            "user": self.user.to_v1(),
            "retweeted_tweet": self.retweeted_tweet.to_v1() if self.retweeted_tweet is not None else None,
            "quoted_tweet": self.quoted_tweet.to_v1() if self.quoted_tweet is not None else None
        }

    def to_v2(self, fields: List[str], expansions: List[str]) -> Dict:
        return {
            "data": {
                "id": self.id,
                "text": self.text
            },
            "includes": {

            }
        }

class User(object):
    
    def __init__(self) -> None:
        self.name = "Anon1"
        self.screenname = "anon1"
        self.id = self.id = floor(random() * 1e10)
        self.created_at = date(2000, 1, 1)

    def to_v1(self) -> Dict:
        return {
            "id": self.id,
            "screenname": self.screenname,
            "name": self.name,
            "created_at": self.created_at
        }

def generate_tweet(
    fields, expansions
):
    tweet = Tweet()
    
    return (tweet.to_v1(), tweet.to_v2(fields, expansions))
