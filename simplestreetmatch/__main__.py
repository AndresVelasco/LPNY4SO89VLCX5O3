import sys
import pdb
import argparse

if sys.version_info [0] < 3:
    from streetcollection import StreetCollection
else:
    from .streetcollection import StreetCollection

from . import defaults

def ratio_from_var2_var1 (row):

    if 'variable1' in row and 'variable2' in row:
        var1 = safeint (row ['variable1'])
        var2 = safeint (row ['variable2'])
        if var1 is not None and var2 is not None:
            return ('{:.2f}'.format (round (var1/float (var2), 2)) if var2 != 0 else 'inf')
        else:
            return ('-')
    else:
        return ('?')

def safeint (x):

    try:
        return (int (x))
    except:
        return (None)

def main (str_args, debug = False):

    if debug:
        pdb.set_trace ()

    parser = argparse.ArgumentParser (description = 'simple address csv matching', epilog = None, formatter_class=argparse.ArgumentDefaultsHelpFormatter, argument_default = None)

    parser.add_argument ('--debug', action = 'store_true')
    parser.add_argument ('--input', action = 'store', nargs = 2, required = True)
    parser.add_argument ('--out', action = 'store', nargs = '?', default = sys.stdout, type = argparse.FileType ('r'))

    args = parser.parse_args (str_args.split ()) if str_args else parser.parse_args ()

    if not debug and args.debug:
        pdb.set_trace ()

    with open (args.input [0], 'r') as f1:
        sc1 = StreetCollection (f1, delimiter = defaults.DELIMITER, quotechar = defaults.QUOTECHAR, key_column_name = defaults.KEY_COLUMN_NAME)
        with open (args.input [1], 'r') as f2:
            sc2 = StreetCollection (f2, delimiter = defaults.DELIMITER, quotechar = defaults.QUOTECHAR, key_column_name = defaults.KEY_COLUMN_NAME)
            sc1.join (sc2, f = args.out, match_column_name = defaults.MATCH_COLUMN_NAME, match_column_fn = ratio_from_var2_var1)
            
if __name__ == '__main__':
    main (None)
