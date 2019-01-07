import argparse
import csv
import sys
import time
import os
from dateutil.parser import parse
from collections import OrderedDict
from shutil import copyfile

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
  ALLIDLIST=[]
  ALRIDLIST=[]
  COUNT=1
  STATUS=100
  with open("banids.csv") as ids:
	  for ID in ids:
		  IDLIST.append(ID)
  sys.stdout.write(str(len(IDLIST))+" BANIDS.CSV RAW\n")
  IDLISTSET=set(IDLIST)
  sys.stdout.write(str(len(IDLISTSET))+" BANIDS.CSV NO DUPES\n")
  IDLIST=[]
  sys.stdout.write(str(len(IDLIST))+" SHOULD BE 0\n")
  with open("allbanids.csv") as ids:
	  for ID in ids:
		  ALLIDLIST.append(ID)
  sys.stdout.write(str(len(ALLIDLIST))+" ALLBANIDS.CSV RAW\n")
  ALLIDLISTSET=set(ALLIDLIST)
  sys.stdout.write(str(len(ALLIDLISTSET))+" ALLBANIDS.CSV NO DUPES\n")
  ALLIDLIST=[]
  sys.stdout.write(str(len(ALLIDLIST))+" SHOULD BE 0\n")
  with open("alreadybanned.csv") as ids:
	  for ID in ids:
		  ALRIDLIST.append(ID)
  sys.stdout.write(str(len(ALRIDLIST))+" ALREADYBANNED.CSV RAW\n")
  ALRIDLISTSET=set(ALRIDLIST)
  sys.stdout.write(str(len(ALRIDLISTSET))+" ALREADYBANNED.CSV NO DUPES\n")
  ALRIDLIST=[]
  sys.stdout.write(str(len(ALRIDLIST))+" SHOULD BE 0\n")

  sys.stdout.write("PERFORMING DIFFERENCE OPTION\n")

  DONE=IDLISTSET.difference(ALLIDLISTSET,ALRIDLISTSET)
  sys.stdout.write(str(len(DONE))+" AFTER REDUCTION\n")
  
  sys.stdout.write("WRITING OUT BANIDS.CSV.CULL\n")

  with open("banids.csv.cull","w") as ids:
    for ID in DONE:
      #sys.stdout.write(ID+"\n")
      ids.write(ID)
  
  sys.stdout.write("COPYING TO BANIDS.CSV\n")
  copyfile("banids.csv.cull","banids.csv")
      
    
  #IDSET=sorter(IDLIST)
  #print len(IDSET)

  #with open("banids.csv","w") as ids:
    #for ID in IDSET:
      #ids.write(ID)

def error(msg, exit_code=1):
    sys.stderr.write("Error: %s\n" % msg)
    exit(exit_code)

def main():

    cull()

if __name__ == "__main__":
    main()
