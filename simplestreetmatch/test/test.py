import unittest

import os
import tempfile
import filecmp

from .. import streetcollection
from ..__main__ import main

class TestStreetCollection (unittest.TestCase):

    def test (self):

        # get all test files from directory
        n = 1 

        while True:

            file1 = os.path.realpath (os.path.join (os.path.dirname (__file__), 'test{}1.csv'.format (n)))
            file2 = os.path.realpath (os.path.join (os.path.dirname (__file__), 'test{}2.csv'.format (n)))
            fileo = os.path.realpath (os.path.join (os.path.dirname (__file__), 'test{}o.csv'.format (n)))

            if os.path.exists (file1):
                with tempfile.NamedTemporaryFile ('wb', delete = True) as f:
                    main ('--input {} {} --out {}'.format (file1, file2, f.name))

                    # check output file and stored output are the same
                    assert (filecmp.cmp (f.name, fileo))
            else:
                break
        
            n += 1

        if n < 2:
            raise Exception ('no test files present?')



if __name__ == '__main__':
    unittest.main ()

