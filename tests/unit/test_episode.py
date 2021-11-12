import pytest

from transcribe.entities import Episode


def test_init_episode_from_transcript_text():
    with open("tests/testdata/episode_1.txt") as fp:
        text = fp.read()

    episode = Episode.from_transcript_text("1", text)
    assert episode.episode_id == "1"
    assert len(episode.transcripts) == 59


@pytest.mark.parametrize(
    "start_time,end_time,expected",
    [
        (21, 24, "Everybody really just about literally everybody was growing Red Delicious."),
        (21, 30, "Everybody really just about literally everybody was growing Red Delicious. This is Dennis courtier. He's the owner of Pepin heights orchard in Lake City, Minnesota."),
    ]
)
def test_get_segment_transcript(start_time, end_time, expected):
    with open("tests/testdata/episode_1.txt") as fp:
        text = fp.read()

    episode = Episode.from_transcript_text("1", text)
    transcript = episode.get_segment_transcript(start_time, end_time)
    assert transcript == expected


@pytest.mark.parametrize(
    "start_time,end_time,expected",
    [
        (480, 482, "when the honeycrisp finally get to"),
    ]
)
def test_get_broken_segment_transcript(start_time, end_time, expected):
    """
    Explanation of this test case.

    The following is the text from 8:00 to 8:04, i.e. from 480 to 484 seconds.
        when the honeycrisp finally get to the store, they do great

    This means that 11 words are spread across 4 seconds. Hence, we should
    return 5.5 words corresponding to the 2 seconds of transcript requested.
    Since, half a word doesn't make sense, we will round up and return 6 words.

    """
    with open("tests/testdata/episode_1.txt") as fp:
        text = fp.read()

    episode = Episode.from_transcript_text("1", text)
    transcript = episode.get_segment_transcript(start_time, end_time)
    assert transcript == expected
