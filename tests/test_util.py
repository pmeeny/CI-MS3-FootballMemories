from football_memories.util import util


def test_generatetimestamp():
    """
    This test asserts the timestamp is in the
    correct format and length
    """
    timestamp = util.generateTimestamp()
    assert (len(timestamp) == 20)
    assert(timestamp.startswith("2021"))
    assert (timestamp.endswith("_"))


def test_getmonthandyear():
    """
    This test asserts the month and year string is in the
    correct format and length
    """
    month, year = util.getMonthAndYear()
    assert (len(month) == 2)
    assert (len(year) == 4)
    assert (year == "2021")
