"""
Philipp Kessling, April 2022,    Leibniz-Institute for Media Research

Test suite for the Twitter V2 API data reader class, aka. TwacapicReader, named after
the tool Twacapic (which conincidentally reads the Twitter V2 API).
"""

# pylint: disable=W0621, C0114, C0115, C0116
import json

from pytest import fixture, skip

from dabapush.Reader.TwacapicReader import TwacapicReader, TwacapicReaderConfiguration


@fixture
def reader(tmp_path) -> TwacapicReader:
    return TwacapicReader(TwacapicReaderConfiguration("test", read_path=str(tmp_path)))


@fixture
def tweet_data():
    return {
        "data": [
            {
                "attachments": {"media_keys": ["16_1211797899316740096"]},
                "author_id": "2244994945",
                "id": "1212092628029698048",
                "referenced_tweets": [
                    {"type": "replied_to", "id": "1212092627178287104"}
                ],
                "text": "We believe the best future version of our API will come from building it",
                "entities": {"mentions": [{"username": "stinky"}]},
            }
        ],
        "includes": {
            "media": [{"media_key": "16_1211797899316740096", "type": "animated_gif"}],
            "users": [
                {"id": "2244994945", "name": "Twitter Dev", "username": "TwitterDev"},
                {"id": "1234566789", "name": "Old Stinky", "username": "stinky"},
            ],
            "tweets": [
                {
                    "author_id": "2244994945",
                    "id": "1212092627178287104",
                    "referenced_tweets": [
                        {"type": "replied_to", "id": "1212092626247110657"}
                    ],
                    "text": "These launches would not be possible without the feedback you "
                    "provided.",
                }
            ],
        },
    }


def test_inheritance():
    """
    This reader should inherit from the Reader-class.
    """
    skip()


def test_file_resolution():
    skip()


def test_read(tmp_path, tweet_data):
    """Should read files correctly."""
    reader = TwacapicReader(
        TwacapicReaderConfiguration(
            "test", read_path=str(tmp_path), emit_references=False
        )
    )
    with open(tmp_path / "test.json", "wt", encoding="utf8") as f:
        json.dump(tweet_data, f)

    records = list(reader.read())
    assert len(records) == 1
    assert records[0].payload.get("id") == "1212092628029698048"


def test_unpack(reader: TwacapicReader, tweet_data):
    """
    Tweets returned by the API are scattered between a few different places, our
    Reader should join the tweet back together.
    """
    result = reader.unpack_tweet(tweet_data["data"][0], tweet_data["includes"])

    assert result is not None


def test_unpack_mentions():
    skip()


def test_unpack_empty_mentions():
    skip()
