from __future__ import annotations
import math
from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True)
class Transcript:
    start: timedelta
    end: timedelta
    text: str

    def get_segment(self, start: timedelta, end: timedelta) -> str:
        """Returns a transcript segment.

        Args:
          start_time: The start time.
          end_time: The end time.

        Returns:
          The transcript segment.

          If the segment requested end time is greater or equal than the start
          time of the next transcript, this means this entire transcript should
          be returned.

          Otherwise, a partial segment is returned. The partial segment is
          computed as follows:

          The following is the text from 8:00 to 8:04, i.e. from 480 to 484
          seconds.
            when the honeycrisp finally get to the store, they do great

          This means that 11 words are spread across 4 seconds. Hence, we should
          return 5.5 words corresponding to the 2 seconds of transcript
          requested. Since, half a word doesn't make sense, we will round up and
          return 6 words.

        """
        if start <= self.start:
            if self.end is None or end >= self.end:
                return self.text

        words = self.text.split()
        words_per_second = len(words) / self.duration_in_s
        seconds_wanted = (end - start).total_seconds()
        count = math.ceil(words_per_second * seconds_wanted)
        if start > self.start:
            return " ".join(words[-count:])
        else:
            return " ".join(words[:count])

    @property
    def duration_in_s(self) -> float:
        return (self.end - self.start).total_seconds()

    def is_within(self, start: timedelta, end: timedelta) -> bool:
        """Returns True if transcript is the range `start`, `end`."""
        if self.end and self.end <= start:
            return False

        if self.start >= end:
            return False

        return True

    @classmethod
    def from_dict(cls, data) -> Transcript:
        data["start"] = str_to_timedelta(data["start"])
        data["end"] = str_to_timedelta(data["end"])
        return cls(**data)


def str_to_timedelta(timestamp) -> timedelta:
    if timestamp is None:
        return None

    minutes, seconds = timestamp.split(":")
    return timedelta(minutes=int(minutes), seconds=int(seconds))
