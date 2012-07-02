# -*- coding: utf-8 -*-

import sys, getopt, csv, time, math, locale
try:
  locale.setlocale(locale.LC_ALL, 'en_US')
except locale.Error:
  locale.setlocale(locale.LC_ALL, 'en_US.utf8')

# given a string find out the type
def get_type(x):
  types = []
  if x == '0' or x == 0:
    types.append("zero")
    types.append("float")
  if x == '' or x == None:
    types.append("empty")
  x = str(x)
  x = x.replace(",", ".")
  try:
    int(x)
    types.append("int")
  except ValueError:
    try:
      float(x)
      types.append("float")
    except ValueError:
      types.append("string")
  return types

def filter_type(rows, t):
  for r in rows:
    if bool(set(t) & set(get_type(r))):
      if not bool(set(t) & set(["string"])):
        yield r.replace(",", ".")
      else:
        yield r

def trim_to_cols(rows, c):
  if isinstance(c, int):
    for i, r in enumerate(rows):
      try:
        yield r[c]
      except:
        print "row %d skipped" % (i)
        print r
  elif isinstance(c, list):
    for r in rows:
      new_r = [r[int(col_index)] for col_index in c]
      yield new_r
  else:
    for r in rows:
      yield r

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

def output_data(f, c, o, t, d, s, v):
  # calculate running time
  start = time.time()
  
  # open input file
  input_file = open(f, 'rU');
  
  # CSV library to sparate file into rows
  # much easier than writing all exceptions from scratch
  csv_reader = csv.reader(input_file, delimiter=d, quotechar='"')
  
  # skip lines
  while(s > 0):
    csv_reader.next()
    s -= 1
  
  # if user specifies only one column remove the rest of the data
  all_rows = trim_to_cols(csv_reader, c)
  
  # if verbose flag set show progress in reading file
  if v:
    all_rows = output_verbose(all_rows)
  
  # strip out unselected types (string, zero, empty, int or float)
  if isinstance(c, int):
    all_rows = filter_type(all_rows, t)
  
  # print output to file...
  if o:
    file_to_write = open(o, "wb")
    for r in all_rows:
      if isinstance(r, list):
        file_to_write.write("\t".join(r)+"\n")
      else:
        file_to_write.write(r+"\n")
  # print to console
  else:
    for r in all_rows:
      print r

def main(file_path, argv):
  # test if file is help
  if file_path == "-h" or file_path == "--help":
    usage()
    sys.exit()
  try:
    opts, args = getopt.getopt(argv, "h:c:o:t:d:s:v", ["help", "columns=", "output", "type", "delimiter", "skip", "verbose"])
  except getopt.GetoptError:
    usage()
    sys.exit(2)
    # todo: print error/usage info
  # set up defaults
  columns, output, type, delimiter, skip, verbose = None, None, "string", "','", 0, False
  for opt, arg in opts:
    if opt in ("-h", "--help"):
      usage()
    if opt in ("-c", "--columns"):
      if "," in arg:
        columns = arg.split(",")
      else:
        columns = int(arg)
    elif opt in ("-d", "--delimiter"):
      delimiter = arg
    elif opt in ("-t", "--type"):
      if arg == "number":
        type = ["int", "float"]
      elif "," in arg:
        type = arg.split(",")
      else:
        type = [arg]
    elif opt in ("-o", "--output"):
      output = arg
    elif opt in ("-s", "--skip"):
      skip = int(arg)
    elif opt in("-v", "--verbose"):
      verbose = True
  
  # get unique types...
  output_data(file_path, columns, output, type, delimiter, skip, verbose)


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