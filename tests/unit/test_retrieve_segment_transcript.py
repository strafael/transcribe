from typing import List

import pytest

from transcribe.entities import Episode
from transcribe.interfaces import EpisodeRepositoryInterface
from transcribe.usecases import RetrieveSegmentTranscript


class FakeRepository(EpisodeRepositoryInterface):
    def __init__(self):
        self._episodes = set()
        with open("tests/testdata/episode_1.txt") as fp:
            text = fp.read()

        episode = Episode.from_transcript_text("episode_1", text)
        self.add(episode)

    def add(self, episode: Episode):
        self._episodes.add(episode)

    def get(self, episode_id: str) -> Episode:
        for e in self._episodes:
            if e.episode_id == episode_id:
                return e

    def list(self) -> List[Episode]:
        return list(self._episodes)


@pytest.mark.parametrize(
    "episode_id,start_time,end_time,expected",
    [
        ("episode_1", 21, 24, "Everybody really just about literally everybody was growing Red Delicious."),
    ]
)
def test_retrieve_segment_transcript(episode_id, start_time, end_time, expected):
    repo = FakeRepository()
    usecase = RetrieveSegmentTranscript(repo)
    result = usecase.execute(episode_id, start_time, end_time)
    assert result == expected


@pytest.mark.parametrize(
    "episode_id,start_time,end_time,expected",
    [
        ("episode_1", 480, 482, "when the honeycrisp finally get to"),
    ]
)
def test_retrive_broken_segment_transcript(episode_id, start_time, end_time, expected):
    """
    Explanation of this test case.

    The following is the text from 8:00 to 8:04, i.e. from 480 to 484 seconds.
        when the honeycrisp finally get to the store, they do great

    This means that 11 words are spread across 4 seconds. Hence, we should
    return 5.5 words corresponding to the 2 seconds of transcript requested.
    Since, half a word doesn't make sense, we will round up and return 6 words.

    """
    repo = FakeRepository()
    usecase = RetrieveSegmentTranscript(repo)
    result = usecase.execute(episode_id, start_time, end_time)
    assert result == expected
