from football_memories.util import util


def test_generatetimestamp() -> object:
    """
    This test asserts the timestamp is in the
    correct format and length
    """
    timestamp = util.generate_timestamp()
    assert (len(timestamp) == 20)
    assert(timestamp.startswith("2021"))
    assert (timestamp.endswith("_"))


def test_getmonthandyear() -> object:
    """
    This test asserts the month and year string is in the
    correct format and length
    """
    month, year = util.get_month_and_year()
    assert (len(month) == 2)
    assert (len(year) == 4)
    assert (year == "2021")
