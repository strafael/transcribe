from __future__ import annotations
import itertools
import math
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

    def get_segment_transcript(self, start_time, end_time) -> str:
        start = timedelta(seconds=start_time)
        end = timedelta(seconds=end_time)
        matches = []
        for transcript, next_transcript in pairwise(self.transcripts):
            if transcript.timestamp < start:
                continue

            if not start <= transcript.timestamp < end:
                break

            text = get_transcript(transcript, next_transcript, start, end)
            matches.append(text)

        return " ".join(matches)

    @classmethod
    def from_transcript_text(cls, episode_id: str, text: str) -> Episode:
        transcripts = []
        for timestamp, text in TRANSCRIPT_PATTERN.findall(text):
            t = Transcript.from_dict(dict(timestamp=timestamp, text=text))
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


def get_transcript(
        t1: Transcript, t2: Transcript, start: timestamp, end:  timestamp
) -> str:
    if t2.timestamp <= end:
        return t1.text

    words = t1.text.split()
    duration_in_s = (t2.timestamp - t1.timestamp).total_seconds()
    words_per_second = len(words) / duration_in_s
    seconds_wanted = (end - t1.timestamp).total_seconds()
    count = math.ceil(words_per_second * seconds_wanted)
    match = " ".join(words[:count])
    return match
