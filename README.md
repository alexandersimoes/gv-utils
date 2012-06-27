gv-utils
========

Utility programs for dealing with big text files (analyze, output, find errors) written in Python.

- - -

Usage
-----

All utilities are used in the following manner:

``python gvu_analysis.py data/my_large_file.csv -c 11 -d ";" -t float -v``

- - -

Flags
-----

-c, --column [n]
  0 based index of the column to operate on. For gvu_export.py a list of columns may be specified with commas e.g. 0,1,2,5 - to operate on columns [0,1,2,5].

-o, --output [/path/to/file.txt]
  File used for output, will be created if it doesn't exist.

-t, --type [int, float, string, zero or empty]
  Specify type as an option.

-d, --delimiter [","]
  Specify the delimiter for the columns of your text file. If none is specifed default is a comma.

-s, --skip [n]
  The number of rows to skip from top of file. If 1 is specified, script assumes first row is column headers.