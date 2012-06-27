# -*- coding: utf-8 -*-

import sys, getopt, csv, time, math, locale
from collections import defaultdict
try:
  locale.setlocale(locale.LC_ALL, 'en_US')
except locale.Error:
  locale.setlocale(locale.LC_ALL, 'en_US.utf8')

# given a string find out the type
def get_type(x):
  if x == 0 or x == '0':
    return "Zero"
  if x == '' or x == None:
    return "Empty"
  x = str(x)
  x = x.replace(",", ".")
  try:
    int(x)
    return "Int"
  except ValueError:
    try:
      float(x)
      return "Float"
    except ValueError:
      return "String"

# generator function to output progress of reading file
def output_verbose(rows):
  logs = range(2, 7)
  for i, r in enumerate(rows):
    # output line if current counter modulo current
    # cutoff = 0
    if (i % math.pow(10, logs[0])) == 0 and i > 0:
      if len(logs) > 1:
        logs.pop(0)
      # print "%d Rows read" % i
      print locale.format("%d", i, grouping=True) + " rows read"
    yield r

# generator function to split rows into bins type
# c = column if specified
def set_types(rows, types, c):
  for r in rows:
    if c:
      types[c][get_type(r)] += 1
    else:
      for i, col in enumerate(r):
        types[i][get_type(col)] += 1
    yield r

# generator function to keep count of unique values by column
# c = column if specified
def set_uniques(rows, uniques, c):
  for r in rows:
    if c:
      uniques[c][r] += 1
    else:
      for i, col in enumerate(r):
        uniques[i][col] +=1
    yield r

# f = file, c = column, d = delimiter, s = num of rows to skip
# v = verobse
def analyze(f, c, d, s, v):
  types = defaultdict(lambda: defaultdict(int))
  uniques = defaultdict(lambda: defaultdict(int))
  col_names = None
  
  # calculate running time
  start = time.time()
  
  # open input file
  input_file = open(f, 'rb');
  
  # CSV library to sparate file into rows
  # much easier than writing all exceptions from scratch
  csv_reader = csv.reader(input_file, delimiter=d, quotechar='"')
  
  # skip lines
  while(s > 0):
    if s == 1:
      col_names = csv_reader.next()
    else:
      csv_reader.next()
    s -= 1
  
  # if user specifies only one column remove the rest of the data
  if c:
    all_rows = (line[c].strip() for line in csv_reader)
  else:
    all_rows = (line for line in csv_reader)
  
  # 
  if v:
    all_rows = output_verbose(all_rows)
  
  # get unique types (string, zero, empty, int, float)
  all_rows = set_types(all_rows, types, c)
  
  # get unqiue values
  all_rows = set_uniques(all_rows, uniques, c)
  
  # get total number of rows
  row_count = reduce(lambda a, b: a+1, all_rows, 0)
  
  ############
  # print summary
  print "\n>>> FILE SUMMARY <<<"
  print "Total rows: " + locale.format("%d", row_count, grouping=True)
  print ""
  
  # for each column print info
  for i, (type_items, unique_items) in enumerate(zip(types.values(), uniques.values())):
    if col_names:
      print "Column %s [%d]:" % (col_names[c], c,)
    else:
      print "Column %d:" % (i,)
    
    print "  Value types:"
    for t, n in type_items.items():
      print "\t>>> %s: %d" % (t, n)
    
    print "  Unique elements: %d" % (len(unique_items.keys()),)
    if (len(unique_items.keys()) < 50):
      for u, n in unique_items.items():
        print "\t>>> %s: %d" % (u, n)
    
    print ""
  
  print "Time to read file: %0.2f minutes" % ((time.time() - start) / 60.0,)
  print ""
  

def usage():
  print "\n>>> USAGE <<<\n"
  print "/path/to/data_file"
  print "\tThe text file to operate on."
  print ""
  print "-c, --column (n)"
  print "\tThe 0 based index of the column to operate on."
  print ""
  print "-d, --delimiter (',')"
  print "\tThe character used to differentiate columns. The default value is a comma ','."
  print ""
  print "-s, --skip (n)"
  print "\tThe number of lines to skip from top of file. The default value is 0."

def main(file_path, argv):
  # test if file is help
  if file_path == "-h" or file_path == "--help":
    usage()
    sys.exit()
  try:
    opts, args = getopt.getopt(argv, "h:c:o:t:d:s:v", ["help", "column=", "output", "type", "delimiter", "skip", "verbose"])
  except getopt.GetoptError:
    usage()
    sys.exit(2)
    # todo: print error/usage info
  # set up defaults
  column, type, delimiter, skip, verbose = None, "string", "','", 0, False
  for opt, arg in opts:
    if opt in ("-h", "--help"):
      usage()
    if opt in ("-c", "--column"):
      column = int(arg)
    elif opt in ("-d", "--delimiter"):
      delimiter = arg
    elif opt in ("-s", "--skip"):
      skip = int(arg)
    elif opt in("-v", "--verbose"):
      verbose = True
  
  print "Running analysis..."
  
  # get unique types...
  analyze(file_path, column, delimiter, skip, verbose)

  # output_distributions(file_path, column, output, delimiter, skip)

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print "Need a file..."
    sys.exit()
  main(sys.argv[1], sys.argv[2:])

  # get_type tests ################
  #################################
  # get type tests
  # print get_type('0')
  # print get_type('asdf')
  # print get_type('123')
  # print get_type('123.4')
  # print get_type('123.42352')
  # print get_type('123,4')
  # print get_type('asdf 235,23')
  # sys.exit()
  #################################