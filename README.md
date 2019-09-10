# The Test

_You may find enclosed two CSV files, related to a listing of stores in one country._
 
_The file "exercise_part_1.csv" contains an id, the address, the category each store belongs to (A, B, C or D) and a "variable1".
"exercise_part_2.csv" contains data about some other "variable2"._

_For this assignment you have to write code and tests (using either Node.js or Python) to save to disk a third CSV file with 4 columns:_ 
_- id_ 
_- var1_ 
_- var2_
_- ratio (var1/var2)_ 
 
_NOTE: take into account that, due to the data in the CSVs coming from different sources,  addresses are not exactly the same in_ 
_both datasets (st. vs street, etc) so they need to be normalized first._
_If for any reason there’s an address that cannot be normalized with a simple algorithm, please explain how it could be normalized_ 
_with more sophisticated techniques._

# Overview

This solution to the technical test is written in python and should preferably be executed with python version 3. It has no external
dependencies.

Python code is available in a module: `simplestreetmatch`, which includes a _main_, accessible as follows:

```
andres@debian9:~/src/LPNY4SO89VLCX5O3$ python -m simplestreetmatch
usage: __main__.py [-h] [--debug] --input INPUT INPUT [--out [OUT]]
__main__.py: error: the following arguments are required: --input
```

If output file is omitted, results are written to standard output.

For example:

```
andres@debian9:~/src/LPNY4SO89VLCX5O3$ python -m simplestreetmatch --input samples/Exercise_data_poi_part_1.csv samples/Exercise_data_poi_part_2.csv | more
id_store;address;variable1;category;variable2;ratio
1;100 High St.;74;A;88;0.84
2;382-384 Brixton Rd;91;A;42;2.17
3;11, little stonegate;13;A;70;0.19
4;corner of pittville & albion street, cheltenham;48;A;85;0.56
5;16 high street, unit 7, grant’s entertainment centre;71;A;70;1.01
...
```

Normalization and record matching logic is delivered by class `simplestreetmatch.streetcollection.StreetCollection` which is described below. 

## Testing

Automatic tests can be found in simplestreetmatch.test.test and are based on stored sets of sample input files and their expected output. For example, there is at the moment a _set number 1_:

```
andres@debian9:~/src/LPNY4SO89VLCX5O3/simplestreetmatch/test$ ls *csv*
test11.csv  test12.csv  test1o.csv
```

Adding more sets does not require changing python code.

Tests can be run with:

```
andres@debian9:~/src/LPNY4SO89VLCX5O3$ python -m unittest discover
/home/andres/src/LPNY4SO89VLCX5O3/simplestreetmatch/test/test.py:25: ResourceWarning: unclosed file <_io.TextIOWrapper name='/tmp/tmpbf3k0r3k' mode='w' encoding='UTF-8'>
  main ('--input {} {} --out {}'.format (file1, file2, f.name))
.
----------------------------------------------------------------------
Ran 1 test in 0.019s

OK
```

# Solution Highlights (StreetCollection)

The solution attempts to match addresses after normalization, but its possible that a production-grade solution would require a best-match approach.

        An instance of this class represents a csv file, loaded from a file object.

        The join method allows merging two instances based on a shared column with name given by key_column_name (address from now on).
        
        The Join operation is actually an 'outer join' with the following highlights:
        - The resulting record has the union of all columns from both instances.
        - Two records are merged into an output one if their normalized key (more on this below) matches exactly. 
          The instance executing the join takes precedence and does not have its values overwritten, in case there is an overlap of columns in both instances.
        - Unmatched records are included, with a default value in the missing record columns.
        - It is possible to add a new column with name and value according to join () arguments.
        - The results of the join operation are written to an output file-object.

        Each record of the file is represented by a tuple of (key, original row, extra_info) where key is a normalized adress used for record matching and extra_info is described below.

        Normalization steps include:
        - Converting to lowercase
        - Extracting <building_name>, a string of non-decimal characters preceding a decimal number. 
          For example: The Cornerhouse in "The Cornerhouse, 12 Trinity Square" or "Dolphin House" in address "Dolphin House, 1 North Street, Guildford"
          The motivation for this was finding adresses in separate files, including and lacking the <building_name>
        - Normalizing street number ranges: two decimal characters separated by whitespace and a separator as provided in defaults.RANGE_SEPARATORS
        - Remove non-word characters (\W in python's re package).
        - Turning any contiguous whitespace chars into a single space.
        - Changing street and road words to st and rd respectively. A production-grade version would require receiving a list of mappings.

        This transformations can be found in StreetCollection.process_row ()

        extra_info is a dictionary with information elements extracted from the original address, relevant for making decisions when comparing two records. 

        At the moment, the following is filled-in:

        - building_name as described above. It is used when comparing two normalized keys (which lack building_name) such that: 
          if there is a match of keys but building_name is present for both and does not match the two records are not considered to match. If one lacks building_name then a match is considered.
        - range_min and range_max, applicable when a range of street numbers is detected. Not used at the moment. For example: "112-114 English Street Carlisle CA3 8ND"

        With the rules above, and the test data provided (Exercise_data_poi_part_1.csv, Exercise_data_poi_part_2.csv), a mismatch is detected for the following two records in files 1 and 2 respectively:
        "46-50 Oldham Street, Northern Quarter" and "46-50 oldham st"

        A possible solution, which I have not implemented, would be: if the adresses do not match but one is contained in the other AND a number is included then consider them matched. 

