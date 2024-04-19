"""
This module contains the Record dataclass, which is used to store the data and additional
"""
import dataclasses
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4


@dataclasses.dataclass
class Record:
    """This dataclass represents a single record in a data set.
    It is used to store the data and additional information about the record and helps to keep
    the data organized.

    The use cases where this class is used are:
    - help reshuffling the data, i.e. based on the source directory name.
    - create audit logs, i.e. to keep track of the data source
      and the time the data was processed.

    Attributes
    ----------
    payload : Dict[str, Any]
        The data of the record.
    source : Optional[Any]
        The source of the record.
    uuid : Optional[str]
        The unique identifier of the record.
    processed_at : datetime
        The time the record was processed.
    children : List["Record"]
        The list of child records of the record.

    Examples
    --------
    >>> record = Record({"key": "value"}, Path())
    >>> record.uuid
    '...'
    >>> record.processed_at
    '...'
    >>> record.payload
    {"key": "value"}
    >>> record.source
    Path()
    >>> record.children
    []

    """

    payload: Dict[str, Any]
    source: Optional[Any] = None
    uuid: Optional[str] = uuid4().hex
    processed_at: datetime = datetime.now()
    children: List["Record"] = dataclasses.field(default_factory=list)

    def split(self, key: str, id_key: Optional[str] = None) -> List["Record"]:
        """Split the record based on a key in the payload.

        Args:
            key (str): The key to split the record on.
            id_key (Optional[str], optional): The key to use as the unique identifier for
            the child records. Defaults to None.

        Returns:
            List[Record]: A list of records.
        """
        if key not in self.payload:
            return []
        if not isinstance(self.payload[key], list):
            return []
        split_payload = [
            Record(
                **{
                    "payload": value,
                    "uuid": value.get(id_key) if id_key else uuid4().hex,
                }
            )
            for value in self.payload[key]
        ]
        self.children.extend(split_payload)

        return split_payload

    def to_log(self):
        """Return a loggable representation of the record."""
        return {
            "uuid": str(self.uuid),
            "processed_at": self.processed_at.isoformat(),
            # We cannot allow the source to be a Record, as it would create a circular reference
            # while serializing the dataclass to JSON.
            "source": str(self.source) if not isinstance(self.source, Record) else None,
            "children": [str(child.uuid) for child in self.children],
        }
