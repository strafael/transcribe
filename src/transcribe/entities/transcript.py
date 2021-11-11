from __future__ import annotations
from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True)
class Transcript:
    timestamp: timedelta
    transcript: str

    @classmethod
    def from_dict(cls, data) -> Transcript:
        hours, minutes = data["timestamp"].split(":")
        delta = timedelta(hours=int(hours), minutes=int(minutes))
        return cls(delta, data["transcript"])
