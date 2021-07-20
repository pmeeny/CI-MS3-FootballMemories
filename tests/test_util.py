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
        timestamp = util.generateTimestamp()
        assert (len(timestamp) == 20)
        assert(timestamp.startswith("2021"))
        assert (timestamp.endswith("_"))
        
    def test_getMonthAndYear():   
        month, year = util.getMonthAndYear()
        assert (len(month) == 2)
        assert (len(year) == 4)
        assert (year == "2021")
        
    #def test_setupPagination():    
    #    offset, per_page, page = util.setupPagination()  
    #    print (offset)
    #    print (per_page)
    #    print (page)
        
        #https://stackoverflow.com/questions/17375340/testing-code-that-requires-a-flask-app-or-request-context
        #https://pythonhosted.org/Flask-Testing/
        
        #coverage run -m pytest
        #coverage report -m
        