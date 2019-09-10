import re
import csv

from . import defaults

class StreetCollection (object):

    def __init__ (self, f, delimiter = ';', quotechar = '"', key_column_name = 'address'):
      
        self.data = []
        self.key_column_name = key_column_name
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.columns = None

        self.load (f)

    def load (self, f):

        reader = csv.DictReader (f, delimiter = self.delimiter, quotechar = self.quotechar)

        n = 0

        for row in reader:
           
            n += 1

            if not self.columns:
                if self.key_column_name not in row:
                    raise Exception ('line #{}: key column {} not present?'.format (n, self.key_column_name))
                self.columns = list (row.keys ())

            self.data.append (self.process_row (row))

        # sort by normalized key
        sorted (self.data, key = lambda x: x [0])

    def process_row (self, row):

        # apply transformations to address:
        # lower
        # whitespace to single space
        # 'typography dash' to regular dash
        # <num> <sep> <num> to <num>-<num>
        # chars <num> <chars> move chars to metadata (building name)
        # street to st
        # punctuation

        extra_info = { }

        key = row [self.key_column_name].lower ()

        # remove space from beginning and end
        key = re.sub (r'^[\s]+', '', key)
        key = re.sub (r'[\s]+$', '', key)

        # extract building name in <building name> <num>
        # MIDDLETON GRANGE SHOPPING CENTRE PARK ROAD HARTLEPOOL TS24 7RZ
        match = re.match (r'(?P<building_name>^[^\d]+[\s]+)[\d]+[\s\W]+', key)
        if match:
            extra_info ['building_name'] = self.cleanse_string (match.group ('building_name'))
            key = key [match.end ('building_name'): ]
            #print ('HAVE BUILDING NAME', extra_info ['building_name'])

        # convert <num> <sep> <num> to <num> to <num> (range)
        match = re.match (r'(?P<range_min>[\d]+)[\s]*(?P<separator>[^\d\s])[\s]*(?P<range_max>[\d]+)', key)
        if match:
            # check that the separator is legit: dash or \u2014 or ...
            extra_info ['range_min'] =  match.group ('range_min')
            extra_info ['range_max'] =  match.group ('range_max')

            if match.group ('separator') in defaults.RANGE_SEPARATORS:
                key = '{}{} to {}{}'.format (key [0: match.start ('range_min')],match.group ('range_min'), match.group ('range_max'), key [match.end ('range_max'): ])

        key = self.cleanse_string (key)

        #print (key, row, extra_info)

        return (key, row, extra_info)

    def cleanse_string (self, s):

        # remove non words
        s = re.sub (r'[^\w\s]', '', s)

        # this could be based on a parameter (list of strings to replace)
        s = re.sub (r'[\s]+street', ' st', s)
        s = re.sub (r'[\s]+road', ' rd', s)

        # convert multiple whitespace to single space
        s = re.sub (r'[\s]+', ' ', s)

        s = re.sub (r'^[\s]+', '', s)
        s = re.sub (r'[\s]+$', '', s)
        return (s) 

    def join (self, sc, f = None, match_column_name = None, match_column_fn = lambda row: '', unmatched_row_value = ''):
        
        data1 = self.data
        data2 = sc.data

        len1 = len (data1)
        len2 = len (data2)

        # build list of all resulting columns
        columns = self.columns 
        columns += [ x for x in sc.columns if x not in self.columns ]
        if match_column_name:
            columns += [ match_column_name ]

        # create function that builds the resulting row from the 2 input ones
        build_out_row = lambda row1, row2 = None: self.build_out_row (row1, row2, match_column_name, match_column_fn)

        i = j = 0 # iterators for each table

        writer = csv.DictWriter (f, columns, restval = unmatched_row_value, delimiter = self.delimiter, quotechar = self.quotechar, lineterminator='\n') if f else None

        writer.writeheader ()

        while True:

            # get the next elements to take into consideration
            el1 = data1 [i] if i < len1 else None
            el2 = data2 [j] if j < len2 else None 

            if not el1 and not el2:
                break

            # if we still have data in 1
            if el1:
                # if data2 is exhausted or next data2 element is larger than data1's
                if not el2 or el1 [0] <= el2 [0]:

                    # IMPORTANT: cope with case: 46-50 Oldham Street[, Northern Quarter]
                    same = el1 and el2 and ( el1 [0] == el2 [0] or el1 [0] in el2 [0] or el2 [0] in el1 [0] )

                    if not el2 or el1 [0] < el2 [0]:
                        #print ('DATA1 UNMATCHED', same, el1, el2)
                        writer.writerow (build_out_row (el1 [1]))

                    elif el2 and el1 [0] == el2 [0]:
                        # if keys are the same, emit together unless bulding names differ
                        if 'building_name' not in el1 [2] or 'building_name' not in el2 [2] or el1 [2] ['building_name'] == el2 [2] ['building_name']:
                            writer.writerow (build_out_row (el1 [1], el2 [1]))
                        else:
                            writer.writerow (build_out_row (el1 [1]))
                            writer.writerow (build_out_row (el2 [1]))
                          
                        j += 1
                        
                    i += 1

                    if el2 and el1 [0] == el2 [0]:
                        continue

            # if we still have data in data2
            if el2:
                #print ('DATA2 UNMATCHED', el1, el2)
                writer.writerow (build_out_row (el2 [1]))
                j += 1

    def build_out_row (self, row1, row2, match_column_name, match_column_fn):
        
        if row2:
            row2.update (row1)
            res = row2
        else:
            res = row1

        # add extra column
        if match_column_name and match_column_fn:
            res [match_column_name] = match_column_fn (res)

        return (res)
                
