from __future__ import annotations
from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True)
class Transcript:
    timestamp: timedelta
    text: str

    @classmethod
    def from_dict(cls, data) -> Transcript:
        minutes, seconds = data["timestamp"].split(":")
        delta = timedelta(minutes=int(minutes), seconds=int(seconds))
        return cls(delta, data["text"])
