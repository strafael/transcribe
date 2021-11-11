from transcribe.entities import Episode


def test_init_episode_from_transcript_text():
    with open("tests/testdata/episode_1.txt") as fp:
        text = fp.read()

    episode = Episode.from_transcript_text("1", text)
    assert episode.episode_id == "1"
    assert len(episode.transcripts) == 59
