import pytest
import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_paginate import Pagination, get_page_args
from football_memories.util import util

if os.path.exists("env.py"):
    import env


def test_generateTimestamp():
    """
    This test asserts the timestamp is in the
    correct format and length
    """
    timestamp = util.generateTimestamp()
    assert (len(timestamp) == 20)
    assert(timestamp.startswith("2021"))
    assert (timestamp.endswith("_"))


def test_getMonthAndYear():
    """
    This test asserts the month and year string is in the
    correct format and length
    """
    month, year = util.getMonthAndYear()
    assert (len(month) == 2)
    assert (len(year) == 4)
    assert (year == "2021")
