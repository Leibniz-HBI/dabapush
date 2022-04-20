"""
Philipp Kessling, April 2022,    Leibniz-Institute for Media Research

Test suite for the Twitter V2 API data reader class, aka. TwacapicReader, named after
the tool Twacapic (which conincidentally reads the Twitter V2 API).
"""
from pytest import fixture, skip, mark
from dabapush.Reader.TwacapicReader import TwacapicReader, TwacapicReaderConfiguration

@fixture
def reader() -> TwacapicReader:
    return TwacapicReader(TwacapicReaderConfiguration('test'))

def test_inheritance():
    """
    This reader should inherit from the Reader-class.
    """
    skip()

def test_file_resolution():
    skip()

def test_unpack(reader: TwacapicReader):
    """
    Tweets returned by the API are scattered between a few different places, our
    Reader should join the tweet back together.
    """
    test_dict = {
        "data": {
            "attachments": {
                "media_keys": [
                    "16_1211797899316740096"
                ]
            },
            "author_id": "2244994945",
            "id": "1212092628029698048",
            "referenced_tweets": [
                {
                    "type": "replied_to",
                    "id": "1212092627178287104"
                }
            ],
            "text": "We believe the best future version of our API will come from building it with YOU. Here’s to another great year with everyone who builds on the Twitter platform. We can’t wait to continue working with you in the new year. https://t.co/yvxdK6aOo2",
            "entities": {
                "mentions": [
                    {"username": "stinky"}
                ]
            }
        },
        "includes": {
            "media": [
                {
                    "media_key": "16_1211797899316740096",
                    "type": "animated_gif"
                }
            ],
            "users": [
                {
                    "id": "2244994945",
                    "name": "Twitter Dev",
                    "username": "TwitterDev"
                },
                {
                    "id": "1234566789",
                    "name": "Old Stinky",
                    "username": "stinky"
                }
            ],
            "tweets": [
                {
                    "author_id": "2244994945",
                    "id": "1212092627178287104",
                    "referenced_tweets": [
                        {
                            "type": "replied_to",
                            "id": "1212092626247110657"
                        }
                    ],
                    "text": "These launches would not be possible without the feedback you provided along the way, so THANK YOU to everyone who has contributed your time and ideas. Have more feedback? Let us know ⬇️ https://t.co/Vxp4UKnuJ9"
                }
            ]
        }
    }
    result = reader.unpack_tweet(
        test_dict["data"],
        test_dict["includes"]
    )

    assert result is not None

def test_unpack_mentions():
    skip()

def test_unpack_empty_mentions():
    skip()
