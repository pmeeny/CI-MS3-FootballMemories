import os
import tempfile

import pytest

from football_memories import create_app

from football_memories.administration import routes

def test_home(self, mongo):
    routes.home()
   
    
#def test_terms_and_conditions():
    #c.terms_and_conditions()