from __future__ import annotations
import itertools
import re
from dataclasses import dataclass
from datetime import timedelta
from typing import List

from .transcript import Transcript

# This matches transcripts from a transcript format
# It matches when a timestamp is followed by a new line, then captures
# everything until the next new line.
TRANSCRIPT_PATTERN = re.compile(r"(\d+:\d+)\s\s\n(.*?)\n")


@dataclass
class Episode:
    episode_id: str
    transcripts: List[Transcript]

    def __hash__(self):
        return hash(self.episode_id)

    def get_segment_transcript(self, start_time: str, end_time: str) -> str:
        """Get the transcript segment within the specified timestamps.

        Args:
          start_time: The start time.
          end_time: The end time.

        Returns:
          The transcript segment.
        """
        start = timedelta(seconds=start_time)
        end = timedelta(seconds=end_time)
        transcripts_in_range = [t for t in self.transcripts if t.is_within(start, end)]
        matches = []
        for transcript in transcripts_in_range:
            matches.append(transcript.get_segment(start, end))

        return " ".join(matches)

    @classmethod
    def from_transcript_text(cls, episode_id: str, text: str) -> Episode:
        transcripts = []
        for t1, t2 in pairwise(TRANSCRIPT_PATTERN.finditer(text)):
            start, text = t1.groups()
            if t2 is None:
                end = None
            else:
                end, _ = t2.groups()

            t = Transcript.from_dict(dict(start=start, end=end, text=text))
            transcripts.append(t)

        return cls(episode_id, transcripts)


def pairwise(iterable):
    """
    Return successive overlapping pairs taken from the input iterable.
    https://docs.python.org/3/library/itertools.html

    """
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.zip_longest(a, b)
