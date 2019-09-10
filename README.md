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

Python code is delivered in a module: @simplestreetmatch@, including a command.

```
andres@debian9:~/src/LPNY4SO89VLCX5O3$ python -m simplestreetmatch
usage: __main__.py [-h] [--debug] --input INPUT INPUT [--out [OUT]]
__main__.py: error: the following arguments are required: --input
```

For example:

```
andres@debian9:~/src/LPNY4SO89VLCX5O3$ python -m simplestreetmatch --input samples/Exercise_data_poi_part_1.csv samples/Exercise_data_poi_part_2.csv | more
id_store;address;variable1;category;variable2;ratio
1;100 High St.;74;A;88;0.84
2;382-384 Brixton Rd;91;A;42;2.17
3;11, little stonegate;13;A;70;0.19
4;corner of pittville & albion street, cheltenham;48;A;85;0.56
5;16 high street, unit 7, grant’s entertainment centre;71;A;70;1.01
6;22-24 the exchange way, chelmsford;25;A;18;1.39
7;11 bridge st;12;A;87;0.14
8;81-91 john bright st;39;A;23;1.70
9;the citrus building, 24 madeira road;31;A;2;15.50
10;8 broad quay;87;A;97;0.90
...
```

No external 
