
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any


class TrackableDataStatus(Enum):
    Initial = 0
    Current = 1

@dataclass
class TrackableData():
    # 1. Store the actual dictionary in a private-by-convention attribute
    _data: dict[TrackableDataStatus, Any] = field(
        default_factory=lambda: {TrackableDataStatus.Initial: None, TrackableDataStatus.Current: None}
    )
    modified: bool = False

    @property
    def data(self) -> dict:
        """Only ever return the CURRENT value for data."""
        return self._data[TrackableDataStatus.Current]

    @data.setter
    def data(self, value: Any):
        """On our first setting, we set the Initial value, otherwise we set CURRENT"""
        # If explicitly clearing the data
        if value is None:
            self._data = {TrackableDataStatus.Initial: None, TrackableDataStatus.Current: None}
            self.modified = False
            return

        # If Initial already has a value, update Current and check if it changed
        if self._data[TrackableDataStatus.Initial] is not None:
            self._data[TrackableDataStatus.Current] = value
            self.modified = (self._data[TrackableDataStatus.Initial] != self._data[TrackableDataStatus.Current])
        else:
            # First time setting data: both initial and current get the same value
            self._data[TrackableDataStatus.Initial] = value
            self._data[TrackableDataStatus.Current] = value
            self.modified = False

    def __str__(self):
        return f"isModified: [{self.modified}] Current: [{self._data[TrackableDataStatus.Current]}] Initial: [{self._data[TrackableDataStatus.Initial]}]"
