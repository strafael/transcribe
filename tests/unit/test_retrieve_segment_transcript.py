import pytest

from transcribe.providers.episode_fake import EpisodeFakeRepository
from transcribe.usecases import RetrieveSegmentTranscript


@pytest.mark.parametrize(
    "episode_id,start_time,end_time,expected",
    [
        ("episode_1", 21, 24, "Everybody really just about literally everybody was growing Red Delicious."),
    ]
)
def test_retrieve_segment_transcript(episode_id, start_time, end_time, expected):
    repo = EpisodeFakeRepository()
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
    repo = EpisodeFakeRepository()
    usecase = RetrieveSegmentTranscript(repo)
    result = usecase.execute(episode_id, start_time, end_time)
    assert result == expected
