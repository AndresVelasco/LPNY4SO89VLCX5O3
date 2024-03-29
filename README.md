# Test Definition

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

If the output file argument is omitted, results are written to standard output.

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

(A full printout of the results is provided in the latest section.)

Normalization and record matching logic is delivered by class `simplestreetmatch.streetcollection.StreetCollection` which is described further below. 

## Tests

Automatic tests can be found in simplestreetmatch.test.test and are based on stored sets of sample input files and their expected output. For example, at the moment there is just a _set number 1_:

```
andres@debian9:~/src/LPNY4SO89VLCX5O3/simplestreetmatch/test$ ls *csv*
test11.csv  test12.csv  test1o.csv
```

Adding more sets does not require changing python code for them to be tested.

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

The solution is based on exact address matching after normalization, although a production-grade solution would require a best-match approach rather than trying to achieve perfect control on normalization (which does not address misspelled and missing words, for instance). A section below is dedicated to drafting possible solutions.

An instance of the StreetCollection class represents a csv file, which is loaded from a file object.

The join method allows merging two instances based on a shared column (`address` in the example).
        
The Join operation is actually an _outer join_ with the following highlights:
* The resulting record has the union of columns from both instances.
* Two records from different instances are merged into a single output if their normalized key (more on this below) matches exactly. 
  The instance executing the join preserves its column values, in case there is an overlap of columns in both instances.
* Unmatched records at any side are included, with a default value in the missing record's columns.
* It is possible to add a new column (ratio in our example) with name and value according to the `join ()` arguments.
* The results of the join operation are written to an output file-object.

Each record of the file is represented by a tuple of `(key, original row, extra_info)` where key is the normalized adress used for record matching and extra_info is described below.

Normalization steps include:
* Converting to lowercase
* Extracting _building_name_, a string that precedes an address. 
  
  For example: The Cornerhouse in "The Cornerhouse, 12 Trinity Square" or "Dolphin House" in address "Dolphin House, 1 North Street, Guildford"
  The motivation for this was finding adresses in separate files, including and lacking the _building_name_. 
  
  Technically, it has been implemented with regular expressions as: _a string of non-decimal characters preceding a decimal number_.
  
* Normalizing street number ranges: two decimal characters separated by optional whitespace and a separator in `defaults.RANGE_SEPARATORS`
       
* Remove non-word characters (\W in python's re package). This filters out punctuation characters typically.

* Turning any contiguous whitespace chars into a single space.

* Changing street and road words to st and rd respectively. A production-grade version would require a list of mappings.

This transformations can be found in `StreetCollection.process_row ()`

`extra_info` in the tuple representation of a record (`(key, original row, extra_info)`) is a dictionary with information elements extracted from the original address, relevant for making decisions when comparing two records. At the moment, the following are filled-in:

* building_name as described above. It is used when comparing two records (whose normalized address lacks building_name) such that: if there is a match of keys but building_name is present for both and does not match the two records are not considered to match. If one lacks building_name then a match is considered.

For example: "1 north street, guildford" and "Dolphin House, 1 North Street, Guildford".

* range_min and range_max, applicable when a range of street numbers is detected. Not used at the moment. For example: "112-114 English Street Carlisle CA3 8ND"

*With the rules above, and the test data provided (Exercise_data_poi_part_1.csv, Exercise_data_poi_part_2.csv), a mismatch is detected for the following two records in files 1 and 2 respectively*:
```
        "46-50 Oldham Street, Northern Quarter" and "46-50 oldham st"
```

A possible solution, which I have not implemented, would be: if the adresses do not match but one is contained in the other AND a number is included then consider them matched. THis would cover this case, but I feel that a production-grade version would require a best-match approach.

A full printout of the results is provided in the latest section.

# Solution At-Scale

There are of course improvements to the type of solution presented here based on more careful examination of possible address patterns, but it would not cover mispelled words, missing or arbitrary abbreviation in long addresses (such as _CASTLEGATE SHOPPING CENTRE HIGH STREET STOCKTON-ON-TEES – TS18 1AF_).

A first pass can always use the exact-match approach so that there are fewer addresses left for a heavier best-match stage.

Among the algorithms and approaches I would explore are the following.

## Leverage on Google Maps API

It should be possible to get geographical coordinates for most of the addresses using Google Maps API, and use them to directly match addresses or as additional criteria in other algorithms.

## Levarage on existing text search tools (ElasticSearch, Solr).

Before implementing a custom best-match algorithm I would explore what existing text-search tools can provide.

## Custom Best-match Algorithm

In short this consists in determining, for every address, the best match in the other set of addresses.

I would consider two approaches:

1. For each address, get the _closest_ according to one or more metrics (string distance algorithms).

Because this can be computationally challenging, it can help that most addresses have a street number, so if we assume that a wrong street number cannot produce a valid match (100 instead of 10 will go undetected), then we only have to compare addresses with the same street number.

This approach is resistant to misspelled words.

2. Get the best-match address based on the count of common words shared by each pair of addresses, weighted by the relevance of each word: a shared word that occurs in many addresses has less relevance than a shared word that occurs in few. 

This approach is especially resistant to missing words such as shopping centre. 

### 


# Full Result Printout

*IMPORTANT*: `ratio` is truncated to 2 decimals and it takes the value '?' for unmatched records and 'inf' when the divident is zero (function `__main__.ratio_from_var2_var1`).

```
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
11;221 – 223 cheltenham road;60;A;42;1.43
12;hodgehouse, 114-116 st mary’s street;71;A;36;1.97
13;1-5 the wardwick, cathedral quarter;89;A;3;29.67
14;16 high street, ealing;31;A;44;0.70
15;guildhall, queen st;13;A;44;0.30
16;1 north street, guildford;91;B;0;inf
17;50 kings st;58;B;59;0.98
18;11 regents court;32;B;0;inf
19;14 the light, the headrow;8;B;68;0.12
20;15 bathhouse lane,  highcross;15;A;100;0.15
21;59-61 hanover street;98;B;69;1.42
22;produce exchange;27;B;74;0.36
23;46-50 oldham st;48;B;;?
;46-50 Oldham Street, Northern Quarter;;;71;?
24;33-35 oxford st;1;B;23;0.04
25;5 mortimer square,  the hub;53;A;39;1.36
26;117 newgate st;85;B;12;7.08
27;8 swan lane, norwich;10;B;68;0.15
28;The Cornerhouse, 12 Trinity Square;19;B;37;0.51
29;12 Friars Entry, Magdalen St;34;B;68;0.50
30;Crystal House, Birley St;6;B;1;6.00
31;36-38 Station Road;1;C;92;0.01
32;1 Guildhall Square;7;C;56;0.12
33;24-26 High St;97;C;44;2.20
34;The Scene, Cleveland Place, 269 High Street, Walthamstow;15;C;62;0.24
35;45-47 Marygate Berwick-Upon-Tweed TD15 1AX;56;C;41;1.37
36;112-114 English Street Carlisle CA3 8ND;68;C;14;4.86
37;36-49 Clifford Road Stanley DH9 0XG;40;C;80;0.50
38;51-53 FRONT STREET CHESTER-LE-STREET DH3 3BH;69;C;27;2.56
39;MIDDLETON GRANGE SHOPPING CENTRE PARK ROAD HARTLEPOOL TS24 7RZ;6;C;37;0.16
40;50-52 NEWGATE STREET BISHOP AUCKLAND DL14 7EQ;72;C;83;0.87
41;12 IVISON LANE WORKINGTON CA14 3DY;55;C;23;2.39
42;49 HIGH STREET REDCAR TS10 3BZ;66;C;80;0.82
43;64 QUEENSWAY BILLINGHAM TS23 2NP;42;C;18;2.33
44;CASTLEGATE SHOPPING CENTRE HIGH STREET STOCKTON-ON-TEES – TS18 1AF;44;C;26;1.69
45;CORNMILL SHOPPING CENTRE CORNMILL CENTRE DARLINGTON – DL1 1LS;98;C;24;4.08
46;26-27 BAXTERGATE WHITBY - YO21 1BW;56;C;63;0.89
47;167 HIGH STREET NORTHALLERTON – DL7 8JZ;34;C;26;1.31
48;20-21 Brunswick Shopping Centre Scarborough - YO11 1UE;55;C;83;0.66
49;107-109 Dalton Road Barrow-In-Furness – LA14 1HZ;83;D;63;1.32
50;Promenades Shopping Centre 31 The Promenades Shopping Centre Bridlington – YO15 2DX;97;D;95;1.02
```
