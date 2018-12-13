import argparse
import csv
import sys
import time
import os
from dateutil.parser import parse
from collections import OrderedDict

def uniq(list):
  last = object()
  for item in list:
    if item == last:
      continue
    yield item
    last = item

def sorter(l):
  return list(uniq(sorted(l)))

def cull():
  if not os.path.isfile("alreadybanned.csv"):
    with open("alreadybanned.csv") as makebanned:
      makebanned.write("")
    print ""

  if not os.path.isfile("banids.csv"):
    with open("banids.csv") as makebanned:
      makebanned.write("")
    print ""

  if not os.path.isfile("allbanids.csv"):
    with open("allbanids.csv") as makebanned:
      makebanned.write("")
  
  IDLIST=[]
  with open("banids.csv") as ids:
	  for ID in ids:
		  IDLIST.append(ID)
  print len(IDLIST)
  with open("allbanids.csv") as allbans:
    for ID in allbans:
      try:
        IDLIST.remove(ID)
        sys.stdout.write("O")
      except:
        sys.stdout.write(".")
  print len(IDLIST)
  with open("alreadybanned.csv") as already:
    for ID in already:
      try:
        sys.stdout.write("O")
        IDLIST.remove(ID)
      except:
        sys.stdout.write(".")
  print len(IDLIST)
  IDSET=sorter(IDLIST)
  print len(IDSET)
  with open("banids.csv","w") as ids:
    for ID in IDSET:
      ids.write(ID)

def error(msg, exit_code=1):
    sys.stderr.write("Error: %s\n" % msg)
    exit(exit_code)

def main():

    cull()

if __name__ == "__main__":
    main()
