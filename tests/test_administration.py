import pytest
import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_paginate import Pagination, get_page_args
from football_memories.administration import routes

if os.path.exists("env.py"):
    import env
    
    #pytest -rP

app = Flask(__name__)

c = app.test_client()
response = c.get('/test/url')   
   
   
    
#def test_terms_and_conditions():
    #c.terms_and_conditions()